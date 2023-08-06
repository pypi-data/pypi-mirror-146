# -*- coding:utf-8 -*-
'''
常用工具.

Version 1.0  2019-09-19 15:56:15 by QiJi
Version 2.0  2021-06-15 09:58:28 by QiJi
    refer [pygeotools](https://github.com/dshean/pygeotools)



GetGeoTransform 含义:
    geoTransform[0]: ulx, 影像左上角横坐标
    geoTransform[1]: xDist, 遥感图像的水平空间分辨率(对于没有旋转的'上北'图像而言)
    geoTransform[2]: rtnX, 旋转参数(在'上北'图像中为0)
    geoTransform[3]: uly, 影像左上角纵坐标
    geoTransform[4]: yDist, 遥感图像的垂直空间分辨率(对于没有旋转的'上北'图像而言)
    geoTransform[5]: rtnY, 旋转参数('上北'图像中为0)

若图像中某一点的行数和列数分别为：row, column
则该点的地理坐标为：
xGeo = geoTransform[0] + column * geoTransform[1] + row * geoTransform[2]
yGeo = geoTransform[3] + column * geoTransform[4] + row * geoTransform[5]

'''
import os
import concurrent.futures as cf
from functools import partial
import numpy as np
from tqdm import tqdm

import PIL
from osgeo import gdal, ogr, osr, gdalnumeric
from pygeotools.lib import geolib, iolib, warplib

from qjdltools.fileop import mkdir_nonexist, filelist, rename_file
from qjdltools.dldata import modify_label
from qjdltools.dlimage import colour_code_label


# **********************************************
# ********** Global default settings ***********
# **********************************************
# CREAT_OPTS = ['COMPRESS=DEFLATE', 'PREDICTOR=2']   # Better zip ratio
CREAT_OPTS = ['COMPRESS=DEFLATE', 'PREDICTOR=1', 'ZLEVEL=1', 'NUM_THREADS=2']  # Speed and zip ratio trade-off
OPEN_OPTS = ['NUM_THREADS=8']


# **********************************************
# ************* GDAL basic tools ***************
# **********************************************
def get_gdal_driver(fileformat):
    fileformat = fileformat.split('.')[-1].lower()
    if fileformat in ['tif', 'tiff']:
        gDriver = gdal.GetDriverByName('GTiff')
    elif fileformat in ['png']:
        gDriver = gdal.GetDriverByName('PNG')
    elif fileformat in ['jpg', 'jpeg']:
        gDriver = gdal.GetDriverByName('JPEG')
    elif fileformat == '':
        gdal.GetDriverByName('MEM')
    return gDriver


def raster_info(img_path):
    """ Load raster image from `img_path` and transform to ndarray.
    Returns:
        if geoInfoarray is Ture: array, geotransform, geoprojection
        if geoInfoarray is Flase: array
    Note: 会将整个数据影像全部读入内存，需要注意图像大小与可用RAM
    """
    # raster = gdal.Open(img_path, options=OPEN_OPTS)
    raster = gdal.Open(img_path, gdal.GA_ReadOnly)

    info = {
        'H': raster.RasterYSize,
        'W': raster.RasterXSize,
        'C': raster.RasterCount,
        'geotransform': list(raster.GetGeoTransform()),
        'geoprojection': raster.GetProjection(),
        'srs': geolib.get_ds_srs(raster)
    }
    return info


# **********************************************
# *********** GDAL | data transform ************
# **********************************************
def imageToArray(image):
    """ Converts a Python Imaging Library array to a
    gdalnumeric image.
    """
    array = gdalnumeric.fromstring(image.tobytes(), 'b')
    array.shape = image.im.size[1], image.im.size[0]
    return array


def arrayToImage(array):
    """ Converts a gdalnumeric array to a
    Python Imaging Library Image.
    """
    im = PIL.Image.frombytes('L', (array.shape[1], array.shape[0]),
                             (array.astype('b')).tobytes())
    return im


def array2raster(img_path, array, geotransform=None, geoprojection=None, create_options=[]):
    """ Create raster (file) from array.
    """
    # Get array basic info
    if 'uint8' in array.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in array.dtype.name:
        datatype = gdal.GDT_Int16
    elif 'uint16' in array.dtype.name:
        datatype = gdal.GDT_UInt16
    elif 'int32' in array.dtype.name:
        datatype = gdal.GDT_Int32
    elif 'uint32' in array.dtype.name:
        datatype = gdal.GDT_UInt32
    elif 'float32' in array.dtype.name:
        datatype = gdal.GDT_Float32
    elif 'float64' in array.dtype.name:
        datatype = gdal.GDT_Float64

    if len(array.shape) == 3:
        rows, cols, band_num = array.shape
    else:
        band_num, (rows, cols) = 1, array.shape

    # Save
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(img_path, cols, rows, band_num, datatype, options=create_options)
    # outRaster = driver.Create(img_path, cols, rows, band_num, options=create_options)

    if geotransform is not None:
        outRaster.SetGeoTransform(geotransform)
    if geoprojection is not None:
        outRaster.SetProjection(geoprojection)

    if len(array.shape) == 2:
        outRaster.GetRasterBand(1).WriteArray(array)
    else:
        for i in range(array.shape[2]):
            outRaster.GetRasterBand(i+1).WriteArray(array[:, :, i])
            outRaster.GetRasterBand(i + 1).FlushCache()  # TODO
    outRaster = None


def raster2array(img_path, geoInfo=False, bands=None):
    """ Load raster image from `img_path` and transform to ndarray.
    Returns:
        if geoInfoarray is Ture: array, geotransform, geoprojection
        if geoInfoarray is Flase: array
    Note: 会将整个数据影像全部读入内存，需要注意图像大小与可用RAM
    """
    # raster = gdal.Open(img_path, options=OPEN_OPTS)
    raster = gdal.Open(img_path, gdal.GA_ReadOnly)
    # Get Geo-Information
    band_num = raster.RasterCount
    geotransform = list(raster.GetGeoTransform())
    geoprojection = raster.GetProjection()

    # Get array
    if band_num == 1:
        band = raster.GetRasterBand(1)
        array = band.ReadAsArray()
    elif bands is None:
        array = raster.ReadAsArray()
        array = array.transpose((1, 2, 0))
    else:
        arrays = []
        for b in bands:
            band = raster.GetRasterBand(b)
            arrays.append(band.ReadAsArray())
        array = np.stack(arrays, axis=2)

    raster = None
    if geoInfo:
        return array, geotransform, geoprojection
    else:
        return array


# **********************************************
# ********** GDAL | croods transform ***********
# **********************************************
def mapToPixel(mX, mY, geoTransform, integer=True):
    """Convert map coordinates to pixel coordinates based on geotransform

    Accepts float or NumPy arrays

    GDAL model used here - upper left corner of upper left pixel for mX, mY (and in GeoTransform)
    """
    mX = np.asarray(mX)
    mY = np.asarray(mY)
    if geoTransform[2] + geoTransform[4] == 0:
        pX = ((mX - geoTransform[0]) / geoTransform[1])  # - 0.5
        pY = ((mY - geoTransform[3]) / geoTransform[5])  # - 0.5
    else:
        pX, pY = applyGeoTransform(mX, mY, invertGeoTransform(geoTransform))

    if integer:
        return round(pX), round(pY)
    return pX, pY


def pixelToMap(pX, pY, geoTransform):
    """Convert pixel coordinates to map coordinates based on geotransform
    Accepts float or NumPy arrays
    GDAL model used here - upper left corner of upper left pixel for mX, mY (and in GeoTransform)
    """
    pX = np.asarray(pX, dtype=float)
    pY = np.asarray(pY, dtype=float)

    # Add 0.5 px offset to account for GDAL model -
    # gt 0,0 is UL corner, pixel 0,0 is center
    # pX += 0.5
    # pY += 0.5
    mX, mY = applyGeoTransform(pX, pY, geoTransform)
    return mX, mY


def reproject_raster(src_pth, dst_pth=None, dstSRS='WGS84'):
    """Reproject a raster image.

    Args:
        dstSRS (str or `osr.SpatialReference()`):
            if dstSRS is str, should be a WellKnownGeogCS, including:
                - “EPSG:n”: where n is the code a Geographic coordinate reference system.
                - “WGS84”: same as “EPSG:4326” (axis order lat/long).
                - “WGS72”: same as “EPSG:4322” (axis order lat/long).
                - “NAD83”: same as “EPSG:4269” (axis order lat/long).
                - “NAD27”: same as “EPSG:4267” (axis order lat/long).
                - “CRS84”, “CRS:84”: same as “WGS84” but with axis order long/lat.
                - “CRS72”, “CRS:72”: same as “WGS72” but with axis order long/lat.
                - “CRS27”, “CRS:27”: same as “NAD27” but with axis order long/lat.

    """
    if dst_pth is None:
        dst_pth = src_pth

    if type(dstSRS) is str:
        srs_name = dstSRS
        dstSRS = osr.SpatialReference()
        dstSRS.SetWellKnownGeogCS(srs_name)

    src_ds = gdal.Open(src_pth, gdal.GA_ReadOnly)
    src_srs = geolib.get_ds_srs(src_ds)
    src_ds = None

    if src_srs.IsSame(dstSRS):
        return
    gdal.Warp(dst_pth, src_pth, dstSRS=dstSRS)


# def _reproject_raster(src_pth, dst_pth, dstSRS=None):
#     print(src_pth, dst_pth)


def reproject_rasters(in_dir, out_dir=None, dstSRS='WGS84', ext='.tif', workers=0):
    """Reproject a raster image.
    """
    if out_dir is None:
        out_dir = in_dir + '_reproj'
    mkdir_nonexist(out_dir)

    if workers:
        executor = cf.ProcessPoolExecutor(max_workers=workers)
        assert type(dstSRS) is str

    futures = []
    for root, dirs, files in tqdm(os.walk(in_dir)):
        cur_out_dir = mkdir_nonexist(root.replace(in_dir, out_dir))
        # Filter image files with specific extension
        files = [name for name in files if name.endswith(ext)]
        for name in files:
            src_pth = os.path.join(root, name)
            dst_pth = os.path.join(cur_out_dir, name)
            if os.path.exists(dst_pth):
                continue

            task = partial(reproject_raster, src_pth, dst_pth, dstSRS)
            if workers > 1:
                futures.append(executor.submit(task))
            else:
                task()

    if workers:
        [future.result() for future in tqdm(futures)]

    print('Finished')


def newGeoTransform(pX, pY, geoTransform):
    """ Update the `GeoTransform` with new up-left point (x, y).
    Args:
        pX: col of up-left point in raster
        pY: row of up-left point in raster
    """
    if type(geoTransform) is tuple:
        geoTransform = list(geoTransform)  # tuple can't be copied
    new_geoTransform = geoTransform.copy()
    ulX = geoTransform[0]
    ulY = geoTransform[3]
    xDist = geoTransform[1]
    yDist = geoTransform[5]

    new_geoTransform[0] = ulX + pX * xDist
    new_geoTransform[3] = ulY + pY * yDist
    return new_geoTransform


#Keep this clean and deal with 0.5 px offsets in pixelToMap
def applyGeoTransform(inX, inY, geoTransform):
    inX = np.asarray(inX)
    inY = np.asarray(inY)
    outX = geoTransform[0] + inX * geoTransform[1] + inY * geoTransform[2]
    outY = geoTransform[3] + inX * geoTransform[4] + inY * geoTransform[5]
    return outX, outY


def invertGeoTransform(geoTransform):
    # we assume a 3rd row that is [1 0 0]
    # compute determinate
    det = geoTransform[1] * geoTransform[5] - geoTransform[2] * geoTransform[4]
    if abs(det) < 0.000000000000001:
        return
    invDet = 1.0 / det
    # compute adjoint and divide by determinate
    outGeoTransform = [0, 0, 0, 0, 0, 0]
    outGeoTransform[1] = geoTransform[5] * invDet
    outGeoTransform[4] = -geoTransform[4] * invDet
    outGeoTransform[2] = -geoTransform[2] * invDet
    outGeoTransform[5] = geoTransform[1] * invDet
    outGeoTransform[0] = (geoTransform[2] * geoTransform[3] - geoTransform[0] * geoTransform[5]) * invDet
    outGeoTransform[3] = (-geoTransform[1] * geoTransform[3] + geoTransform[0] * geoTransform[4]) * invDet
    return outGeoTransform


def geom_transform(geom, t_srs):
    """Transform a geometry in place
    """
    s_srs = geom.GetSpatialReference()
    s_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    if not s_srs.IsSame(t_srs):
        ct = osr.CoordinateTransformation(s_srs, t_srs)
        geom.Transform(ct)
        geom.AssignSpatialReference(t_srs)
    return geom


def cal_overlap_area(fn1, fn2):
    """cal the overlap area of two input raster data.
    Note: Use SpatialReference of `fn1` for calculations
    Parameters:
        fn1: filename of input raster (target SpatialReference)
        fn2: filename of another input raster

    Returns:
        area of overlap
    """
    ds = gdal.Open(fn1, gdal.GA_ReadOnly)
    srs1 = geolib.get_ds_srs(ds)
    db = gdal.Open(fn2, gdal.GA_ReadOnly)
    srs2 = geolib.get_ds_srs(db)

    # Get geom polys
    xmin, ymin, xmax, ymax = geolib.ds_extent(ds)
    wkt = "POLYGON (({} {}, {} {}, {} {}, {} {}, {} {}))".format(
        xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin, xmin, ymin)
    poly1 = ogr.CreateGeometryFromWkt(wkt)
    poly1.AssignSpatialReference(srs1)

    xmin, ymin, xmax, ymax = geolib.ds_extent(db)
    wkt = "POLYGON (({} {}, {} {}, {} {}, {} {}, {} {}))".format(
        xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin, xmin, ymin)
    poly2 = ogr.CreateGeometryFromWkt(wkt)
    poly2.AssignSpatialReference(srs2)
    if not srs1.IsSame(srs2):
        # Default to using first raster's SpatialReference
        srs1.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        srs2.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        tr = osr.CoordinateTransformation(srs2, srs1)
        poly2.Transform(tr)
    # print(poly1.ExportToWkt())
    # print(poly2.ExportToWkt())

    intersect = poly1.Intersection(poly2)
    return intersect.GetArea()


def get_raster_geomploy(src_ds, ref_srs, verbose=False):
    """ Get geom ploy of input raster (path or loaded-ds)
    in ref_srs.

    Args:
        src_ds:
            (string) the path of raster
            (object) the loaded raster ds
        ref_srs: the refence projection

    Returns:
        ploy: geom ploy of input raster
    """
    if type(src_ds) is str:
        src_ds = gdal.Open(src_ds, gdal.GA_ReadOnly)

    srs = geolib.get_ds_srs(src_ds)
    srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

    # Get ds_extent in same projection
    if srs.IsSame(ref_srs):
        xmin, ymin, xmax, ymax = geolib.ds_extent(src_ds)
    else:
        xmin, ymin, xmax, ymax = geolib.ds_extent(src_ds, ref_srs)
    wkt = "POLYGON (({} {}, {} {}, {} {}, {} {}, {} {}))".format(
        xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin, xmin, ymin)
    poly = ogr.CreateGeometryFromWkt(wkt)
    poly.AssignSpatialReference(srs)

    if verbose:
        print(wkt)
        print(poly.ExportToWkt())
    return poly


# **********************************************
# ********* Image processing | spatial *********
# **********************************************
def resample_raster(src_pth, dst_pth=None, scale=1, hw=None,
                    create_options=None):
    """ Resample a raster image. Default is Nearest.

    Args:
        scale: newH = orgH * scale, newW = orgW * scale
        hw: (newH, newW)
    """
    if create_options is None:
        create_options = CREAT_OPTS

    src_ds = gdal.Open(src_pth, -1)

    if hw is None:
        hscale = wscale = scale
    else:
        hscale = hw[0] / src_ds.RasterYSize
        wscale = hw[1] / src_ds.RasterXSize
    out_rows = int(src_ds.RasterYSize * hscale)  # scale=1/5: 2m -> 10m
    out_cols = int(src_ds.RasterXSize * wscale)

    num_bands = src_ds.RasterCount
    dataType = src_ds.GetRasterBand(1).DataType

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(dst_pth, out_cols, out_rows,
                                 num_bands, dataType, options=create_options)
    out_ds.SetProjection(src_ds.GetProjection())
    geotransform = list(src_ds.GetGeoTransform())
    geotransform[1] /= wscale  # col resolution
    geotransform[5] /= hscale  # row resolution
    out_ds.SetGeoTransform(geotransform)

    dst_ds = src_ds.ReadRaster(buf_xsize=out_cols, buf_ysize=out_rows)
    out_ds.WriteRaster(0, 0, out_cols, out_rows, dst_ds)
    out_ds.FlushCache()


def resample_rasters(in_dir, out_dir=None, scale=1, hw=None,
                     ext='.tif', create_options=None):
    """ Resample all the images under `in_dir`,
    and output the result at `out_dir`.
    Default is Nearest.

    Args:
        scale: newH = orgH * scale, newW = orgW * scale
        hw: (newH, newW)
    """
    if out_dir is None:
        out_dir = in_dir
    mkdir_nonexist(out_dir)

    # Walk the dir of data
    for root, dirs, files in tqdm(os.walk(in_dir)):
        cur_out_dir = mkdir_nonexist(root.replace(in_dir, out_dir))

        # Filter image files with specific extension
        files = [name for name in files if name.endswith(ext)]
        for name in files:
            src_pth = os.path.join(root, name)
            dst_pth = os.path.join(cur_out_dir, name)
            resample_raster(src_pth, dst_pth, scale, hw, create_options)
    print('Finished!!!')


# **********************************************
# ********* Image processing | color ***********
# **********************************************
def linear_stretch(image, scale=0.01, channel_wise=False):
    # dtype = image.dtype
    if image.shape == 2 or (not channel_wise):
        minL, maxL = 0, 0
        hist = np.unique(image)

        pixel_total = image.size
        num_pixel_low = int(pixel_total * scale)
        num_pixel_up = int(pixel_total * (1-scale))

        minL, maxL = 0, 0
        hist = np.bincount(image.flatten())
        pixel_cumul = 0
        for L, num in enumerate(hist):
            pixel_cumul += num
            if pixel_cumul >= num_pixel_low:
                minL = L
                break

        pixel_cumul = pixel_total
        for L in range(0, hist.shape[0])[::-1]:
            pixel_cumul -= num
            if pixel_cumul <= num_pixel_up:
                maxL = L
                break

        image = np.clip((255.0*(image-minL)/(maxL-minL)), 0, 255).astype(np.uint8)
    else:
        H, W, band_num = image.shape
        new_image = []
        for b in range(band_num):
            band = image[:, :, b]
            pixel_total = band.size
            num_pixel_low = int(pixel_total * scale)
            num_pixel_up = int(pixel_total * (1-scale))

            minL, maxL = 0, 0
            hist = np.bincount(band.flatten())
            pixel_cumul = 0
            for L, num in enumerate(hist):
                pixel_cumul += num
                if pixel_cumul >= num_pixel_low:
                    minL = L
                    break

            pixel_cumul = pixel_total
            for L in range(0, hist.shape[0])[::-1]:
                pixel_cumul -= hist[L]
                if pixel_cumul <= num_pixel_up:
                    maxL = L
                    break
            # band = np.clip(band, minL, maxL)
            band = np.clip(255.0*(band-minL)/(maxL-minL), 0, 255).astype(np.uint8)
            new_image.append(band)
        image = np.stack(new_image, axis=2)
    return image


def histogram(array, L=256):
    """
    Histogram function for multi-dimensional array.
    a = array
    bins = range of numbers to match
    """
    bins = range(0, L)
    fa = array.flat
    n = gdalnumeric.searchsorted(gdalnumeric.sort(fa), bins)
    n = gdalnumeric.concatenate([n, [len(fa)]])
    hist = n[1:]-n[:-1]
    return hist


def hist_stretch(image, L=256):
    """
    Performs a histogram stretch on a gdalnumeric array image.
    image: PIL.Image object
    """
    import operator
    from functools import reduce

    hist = histogram(image)
    im = arrayToImage(image)
    lut = []
    for b in range(0, len(hist), L):
        # step size
        step = reduce(operator.add, hist[b:b+L]) / (L-1)
        # create equalization lookup table
        n = 0
        for i in range(L):
            lut.append(n / step)
            n = n + hist[i+b]
        im = im.point(lut)
    return imageToArray(im)


# **********************************************
# *********** Inter-raster operation ***********
# **********************************************
def multi_ds_intersection_extent(
        src_fn_list, ref='first', overlap_ref='public',
        verbose=False):
    """Parse the intersection of input rasters,
    and return the ds_list and overlap_extents of those rasters.

    Parameters:
        src_ds_list : list of raster filenames.
        ref: ['first', 'last']
            Default to using first raster as reference
        overlap_ref: ['first', 'last', 'public']
            'first': use the extent of first raster as overlap area
            'last': use the extent of last raster as overlap area
            'pulic': use the extent of intersect of all rasters

    Returns:
        ds_list: input ds list
        overlap_extents: the extents of overlap areas
    """

    if not iolib.fn_list_check(src_fn_list):
        raise ValueError('Missing input file(s)')

    src_ds_list = [gdal.Open(fn, gdal.GA_ReadOnly) for fn in src_fn_list]

    t_srs = warplib.parse_srs(ref, src_ds_list)
    t_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    if verbose:
        print("Projection: '{}'".format(t_srs.ExportToProj4()))

    # * Get geom polys *
    srs_list = []
    geom_polys = []
    for src_ds in src_ds_list:
        src_srs = geolib.get_ds_srs(src_ds)
        src_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        srs_list.append(src_srs)
        geom_polys.append(get_raster_geomploy(src_ds, t_srs))

    # * Get intersection *
    if overlap_ref not in ['first', 'last', 'public']:
        overlap_ref = 'public'

    if overlap_ref == 'first':
        intersect = geom_polys[0]
    elif overlap_ref == 'last':
        intersect = geom_polys[-1]
    else:  # Public overlap
        intersect = None
        for i in range(len(geom_polys)-1):
            if i == 0:
                intersect = geom_polys[i].Intersection(geom_polys[i+1])
            else:
                intersect = intersect.Intersection(geom_polys[i+1])
    overlap_thr = intersect.GetArea()

    if verbose:
        print(intersect.ExportToWkt())

    # * Get intersection extent of each raster *
    dst_extents = []
    for i, (src_ds, src_srs) in enumerate(zip(src_ds_list, srs_list)):

        if intersect.Intersection(geom_polys[i]).GetArea() < overlap_thr:
            continue
        if src_srs.IsSame(t_srs):
            overlap = intersect
        else:
            overlap = geom_transform(intersect.copy(), src_srs)

        extent = geolib.geom_extent(overlap)  # extend in src_srs
        # [ulx, lry, lrx, uly] 2 [ulx, uly, lrx, lry]
        extent = [extent[0], extent[3], extent[2], extent[1]]
        dst_extents.append(extent)

    return {'ds_list': src_ds_list, 'overlap_extents': dst_extents}


def multi_ds_intersection(src_fn_list, out_dir=None, ref='first', r='cubic',
                          overlap_ref='public', save_ref=True,
                          dst_ext='', force_update=False, verbose=False):
    """Parse the intersection of input rasters,
    and .

    Parameters:
        src_ds_list : list of raster filenames.
        src_ds_list : list of raster dataset.
        ref: ['first', 'last']
            Default to using first raster as reference
        r: resample algorithm
            ['near', 'bilinear', 'cubic', 'cubicspline', 'average']
        overlap_ref: ['first', 'last', 'public']
            'first': use the extent of first raster as overlap area
            'last': use the extent of last raster as overlap area
            'pulic': use the extent of intersect of all rasters

    """
    if not iolib.fn_list_check(src_fn_list):
        raise ValueError('Missing input file(s)')
    if out_dir:
        mkdir_nonexist(out_dir)

    src_ds_list = [gdal.Open(fn, gdal.GA_ReadOnly) for fn in src_fn_list]

    t_srs = warplib.parse_srs(ref, src_ds_list)
    t_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    if verbose:
        print("Projection: '{}'".format(t_srs.ExportToProj4()))

    # * Get geom polys *
    srs_list = []
    geom_polys = []
    for src_ds in src_ds_list:
        srs_list.append(geolib.get_ds_srs(src_ds))
        geom_polys.append(get_raster_geomploy(src_ds, t_srs))

    # * Get intersection *
    if overlap_ref not in ['first', 'last', 'public']:
        overlap_ref = 'public'

    if overlap_ref == 'first':
        intersect = geom_polys[0]
    elif overlap_ref == 'last':
        intersect = geom_polys[-1]
    else:  # Public overlap
        intersect = None
        for i in range(len(geom_polys)-1):
            if i == 0:
                intersect = geom_polys[i].Intersection(geom_polys[i+1])
            else:
                intersect = intersect.Intersection(geom_polys[i+1])
    # print(intersect.ExportToWkt())
    extent = geolib.geom_extent(intersect)  # extend in t_srs
    overlap_thr = intersect.GetArea()

    skip_ids = []
    if not save_ref:
        skip_ids.append({'first': 0, 'last': len(src_fn_list)}[ref])

    # * Save overlap from each raster *
    if out_dir:
        driver = gdal.GetDriverByName('GTiff')
    else:
        driver = iolib.mem_drv

    gra = warplib.parse_rs_alg(r)

    dst_rasters = []
    for i, (src_ds, src_srs) in enumerate(zip(src_ds_list, srs_list)):
        if i in skip_ids:
            continue

        # Get dst raster path
        dst_name = os.path.basename(src_fn_list[i])
        if dst_ext:
            dst_name = rename_file(dst_name, extension=dst_ext)

        if out_dir:
            dst_fn = os.path.join(out_dir, dst_name)
            if os.path.exists(dst_fn) and not force_update:
                continue
        else:
            dst_fn = ''  # This is a dummy fn if only in mem

        if intersect.Intersection(geom_polys[i]).GetArea() < overlap_thr:
            continue

        src_gt = src_ds.GetGeoTransform()
        src_dt = src_ds.GetRasterBand(1).DataType
        res = geolib.get_res(src_ds, t_srs=t_srs, square=True)[0]

        # Compute output image dimensions
        dst_nl = int(round((extent[3]-extent[1]) / res))  # rows
        dst_ns = int(round((extent[2]-extent[0]) / res))  # cols
        dst_gt = [extent[0], res, src_gt[2], extent[3], src_gt[4], -res]
        if verbose:
            print('nl: %i ns: %i res: %0.3f' % (dst_nl, dst_ns, res))

        dst_ds = driver.Create(dst_fn, dst_ns, dst_nl, src_ds.RasterCount, src_dt)
        dst_ds.SetProjection(t_srs.ExportToWkt())
        dst_ds.SetGeoTransform(dst_gt)
        for n in range(1, src_ds.RasterCount+1):
            b = dst_ds.GetRasterBand(n)
            b.SetNoDataValue(0)
            b.Fill(0)

        gdal.ReprojectImage(src_ds, dst_ds, src_srs.ExportToWkt(), t_srs.ExportToWkt(),
                            gra, 0.0, 0.0, None)

        dst_rasters.append(dst_ds)
        # dst_ds = None
    return dst_rasters


def crop_by_rowcol(img_path, save_path, crop_info, create_options=None, fileformat='tif'):
    ''' Crop patch(s) from big image with specific row and cols information and save it.
    Note: row - Y axis; col - X axis
    Args:
        save_path: file path(s) to save cropped result, one string of a list of strings for multi-cropping.
        crop_info: one crop_info [row_start, col_start, out_H, out_W] for single cropping,
            or a list of crop_info for multi-cropping.

    '''
    if type(crop_info[0]) != list:
        crop_info = [crop_info]
    if type(save_path) != list:
        save_path = [save_path]
    assert len(crop_info) == len(save_path)
    for spath in save_path:
        mkdir_nonexist(os.path.dirname(spath))

    if create_options is None:
        create_options = CREAT_OPTS

    src_ds = gdal.Open(img_path)
    if src_ds is None:
        ValueError('Cannot open %s!' % img_path)

    # Get basic information about image
    cols = src_ds.RasterXSize
    rows = src_ds.RasterYSize
    num_bands = src_ds.RasterCount

    dataType = src_ds.GetRasterBand(1).DataType
    # print('type', dataType)

    geoProj = src_ds.GetProjection()
    geoTrans = src_ds.GetGeoTransform()

    # Crop
    for (s_pth, c_inf) in zip(save_path, crop_info):
        fname, extn = os.path.splitext(s_pth)

        row_start, col_start, out_H, out_W = c_inf

        if row_start >= rows or row_start < 0:
            ValueError('The specified row_start (%f) is outside the image.' % row_start)
        if col_start >= cols or col_start < 0:
            ValueError('The specified col_start (%f) is outside the image.' % col_start)
        if col_start + out_W >= cols or row_start + out_H >= rows:
            ValueError('The specified crop area (%f, %f) is out of the image range.' % (
                       out_H, out_W))

        patch_ds = src_ds.ReadRaster(xoff=col_start, yoff=row_start, xsize=out_W, ysize=out_H)
        # Get image dirver
        gDriver = get_gdal_driver(extn[1:])

        # Save
        out_ds = gDriver.Create(s_pth, out_W, out_H, num_bands, dataType, options=create_options)
        out_ds.SetProjection(geoProj)
        # out_ds.SetGeoTransform(pixel2world(geoTrans, col_start, row_start))
        out_ds.SetGeoTransform(newGeoTransform(col_start, row_start, geoTrans))

        out_ds.WriteRaster(0, 0, out_W, out_H, patch_ds)
        out_ds.FlushCache()


def crop_by_coords(img_path, save_path, crop_info, create_options=None):
    """ Crop a path from big image with specific Lan and Lng infomation and save it (in same fileformat).
    Multi-cropping is supported.
    Note: lat - X axis - W, lng - Y axis - H

    Args:
        save_path: file path(s) to save cropped result, one string of a list of strings for multi-cropping.
        crop_info: one crop_info - [lat_start, lng_start, out_lat, out_lng]
            or [lat_start, lng_start, out_lat, out_lng, out_W, out_H] for single cropping,
            or a list of crop_info for multi-cropping.
    """
    if type(crop_info[0]) != list:
        crop_info = [crop_info]
    if type(save_path) != list:
        save_path = [save_path]
    assert len(crop_info) == len(save_path)

    stride = 40000  # Set max stride to load into RAM

    for spath in save_path:
        mkdir_nonexist(os.path.dirname(spath))
    if create_options is None:
        create_options = CREAT_OPTS

    # Open file
    src_ds = gdal.Open(img_path)
    if src_ds is None:
        ValueError('Cannot open %s!' % (img_path))

    # Get basic information about image
    cols = src_ds.RasterXSize  # W
    rows = src_ds.RasterYSize  # H
    num_bands = src_ds.RasterCount  # C

    dataType = src_ds.GetRasterBand(1).DataType
    # print('type', dataType)

    geoProj = src_ds.GetProjection()
    geoTrans = src_ds.GetGeoTransform()
    ulX, xDist, rtnX, ulY, rtnY, yDist = geoTrans
    if rtnX != 0 or rtnY != 0:
        ValueError('Roated image is not supported yet!')

    out_crop_info = []

    # Crop
    for (s_pth, c_inf) in zip(save_path, crop_info):
        fname, extn = os.path.splitext(s_pth)
        # Cal image coordinates based on latitude and longitude
        if len(c_inf) == 4:
            lat_start, lng_start, out_lat, out_lng = c_inf
            out_W = round(out_lat / xDist)
            out_H = round(-out_lng / yDist)
        elif len(c_inf) == 6:
            lat_start, lng_start, out_lat, out_lng, out_W, out_H = c_inf
        else:
            ValueError('Wrong length of crop_info!')

        # Cal geoTransforms
        x_start = round((lat_start - ulX) / xDist)  # 无论如何都会产生偏移
        y_start = round((lng_start - ulY) / yDist)  # TODO:考虑保留小数位的像素用于修正裁剪后的影像地理信息

        # TODO: If roate?
        if x_start >= cols:
            ValueError('The specified start_lng (%f) is outside the image.' % lat_start)
        elif x_start < 0:
            out_W += x_start
            x_start, lat_start = 0, ulX
            # crop_by_coords()
        if y_start >= rows:
            ValueError('The specified start_lng (%f) is outside the image.' % lng_start)
        elif y_start < 0:
            out_H += y_start
            y_start, lng_start = 0, ulY
        out_W = min(out_W, cols - x_start)
        out_H = min(out_H, rows - y_start)
        # if x_start + out_W >= cols or y_start + out_H >= rows:
        #     ValueError('The specified crop area (%f, %f) is out of the image range.' % (out_lat, out_lng))

        geoTrans = [lat_start, xDist, rtnX, lng_start, rtnY, yDist]  # update geotrans

        # Get image dirver
        gDriver = get_gdal_driver(extn[1:])

        # Save
        out_ds = gDriver.Create(s_pth, out_W, out_H, num_bands, dataType, options=create_options)
        out_ds.SetProjection(geoProj)
        out_ds.SetGeoTransform(geoTrans)

        if out_W > stride or out_H > stride:
            # 如果裁剪区域过大则需要分块儿读取
            for y in range(0, out_H, stride):
                y_size = min(stride, out_H - y)
                for x in range(0, out_W, stride):
                    x_size = min(stride, out_W - x)
                    patch_ds = src_ds.ReadRaster(xoff=x+x_start, yoff=y+y_start, xsize=x_size, ysize=y_size)
                    out_ds.WriteRaster(x, y, x_size, y_size, patch_ds)
        else:
            patch_ds = src_ds.ReadRaster(xoff=x_start, yoff=y_start, xsize=out_W, ysize=out_H)
            out_ds.WriteRaster(0, 0, out_W, out_H, patch_ds)
        out_ds.FlushCache()

        out_crop_info.append([lat_start, lng_start, 0, 0, out_W, out_H])

    return out_crop_info


def crop_by_masks(target_path, mask_path, save_path, create_options=None):
    """ Crop a patch from big image with specific image with coordinates info and save it.

    Args:
        target_path: The file path of target image to be croped.
        mask_path: The file path(s) of mask image to crop the target,
            could be a list of paths of mask files for multi-cropping.
        save_path: file path(s) to save cropped result.
    """
    out_dir = os.path.dirname(save_path)
    mkdir_nonexist(out_dir)

    # Get crop info. from mask
    if type(mask_path) != list:
        mask_path = [mask_path]
    if type(save_path) != list:
        save_path = [save_path]
    assert len(mask_path) == len(save_path)

    if create_options is None:
        create_options = CREAT_OPTS

    crop_infos = []
    for (m_pth, s_pth) in zip(mask_path, save_path):
        # Open file
        src_ds = gdal.Open(m_pth)
        if src_ds is None:
            ValueError('Cannot open mask: %s!' % (m_pth))

        cols = src_ds.RasterXSize  # W
        rows = src_ds.RasterYSize  # H
        ulX, xDist, rtnX, ulY, rtnY, yDist = src_ds.GetGeoTransform()
        crop_infos.append([ulX, ulY, xDist*cols, -yDist*rows, cols, rows])

    out_crop_info = crop_by_coords(target_path, save_path, crop_infos, create_options)
    # 如果 mask无法被target完全包含，则取两者交集
    new_save_path = [mp.replace('Org_images', 'Org_images_extract') for mp in mask_path]
    # new_save_path = r'G:/Data Bank/GLC/Org_images_test/'
    for m_pth, s_pth, c_info in zip(mask_path, new_save_path, out_crop_info):
        src_ds = gdal.Open(m_pth)
        cols = src_ds.RasterXSize  # W
        rows = src_ds.RasterYSize  # H
        if cols == c_info[4] and rows == c_info[5]:
            continue
        crop_by_coords(m_pth, s_pth, c_info, [])
    # Finish


# **********************************************
# **************** Useful tools ****************
# **********************************************
def crop_imgs(image_dir,
              crop_params,
              out_dir=None,
              create_options=None,
              fileformat='tif',
              log_path=None,
              ifPad=False):
    ''' Slide crop images into small piece and save them.
    Note: not pad yet.
    '''
    if out_dir is None:
        out_dir = image_dir
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    crop_h, crop_w, stride = crop_params
    if create_options is None:
        create_options = CREAT_OPTS
    gDriver = get_gdal_driver(fileformat)
    if '.' not in fileformat:
        fileformat = '.' + fileformat

    name2world = {}  # log dict
    image_names = sorted(os.listdir(image_dir))[:1]
    # for name in tqdm(image_names):
    for name in image_names:
        # Open dataset (not load into RAM)
        # st = time.time()
        src_ds = gdal.Open(image_dir + '/' + name)
        if src_ds is None:
            ValueError('Cannot open %s!' % (image_dir + '/' + name))
        # print('Time cost - Open: %.4fs' % (time.time() - st))

        # Get basic information about image
        fname, _ = os.path.splitext(name)

        cols = src_ds.RasterXSize  # W
        rows = src_ds.RasterYSize  # H
        num_bands = src_ds.RasterCount  # C

        dataType = src_ds.GetRasterBand(1).DataType
        # print('type', dataType)

        geoProj = src_ds.GetProjection()
        geoTrans = src_ds.GetGeoTransform()

        # Crop and save
        y = 0  # y is H(row)
        for i in range((rows-crop_h)//stride + 1):
            x = 0  # x is W(col)
            for j in range((cols - crop_w)//stride + 1):
                # crop and load into RAM (10000x10000x3 uint8 is about 500MB)
                patch_ds = src_ds.ReadRaster(xoff=x,
                                             yoff=y,
                                             xsize=crop_w,
                                             ysize=crop_h)
                # save
                save_name = '%s_%d_%d%s' % (fname, (i+1), (j+1), fileformat)
                out_ds = gDriver.Create(
                    out_dir+'/'+save_name, crop_h, crop_w, num_bands, dataType,
                    options=create_options)

                out_ds.SetProjection(geoProj)
                # out_ds.SetGeoTransform(pixel2world(geoTrans, x, y))
                out_ds.SetGeoTransform(newGeoTransform(x, y, geoTrans))

                out_ds.WriteRaster(0, 0, crop_h, crop_w, patch_ds)
                out_ds.FlushCache()

                if log_path is not None:
                    name2world[save_name] = [geoTrans, geoProj]
                if not os.path.exists(out_dir+'/'+save_name):
                    print('Fail to create file - %s!' % (out_dir+'/'+save_name))

                x += stride
            y += stride
    if log_path is not None:
        with open(log_path, 'w') as f:
            f.write(name2world)


def labels_visualize(label_dir,
                     mCategory,
                     out_dir=None,
                     create_options=None,
                     fileformat='tif'):
    """ Visualize all labels in `label_dir`.
    Note: mCategory can be seen in category.py
    """
    if out_dir is None:
        out_dir = label_dir
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if create_options is None:
        create_options = CREAT_OPTS

    for name in sorted(os.listdir(label_dir)):
        # Load data
        lbl_ds = gdal.Open(label_dir + '/' + name, gdal.GA_ReadOnly)
        lbl_band = lbl_ds.GetRasterBand(1)  # 只取一个波段
        lbl = lbl_band.ReadAsArray()

        geoProj = lbl_ds.GetProjection()
        geoTrans = lbl_ds.GetGeoTransform()

        # Visualization
        lbl = modify_label(lbl, mCategory.table, mCategory.num - 1)
        lbl_vis = colour_code_label(lbl, mCategory.color_table)

        # Save
        gDriver = get_gdal_driver(fileformat)
        out_ds = gDriver.Create(out_dir + '/' + name, lbl.shape[1], lbl.shape[0], 3, options=create_options)
        out_ds.SetGeoTransform(geoTrans)
        out_ds.SetProjection(geoProj)

        for i in range(lbl_vis.shape[2]):
            out_ds.GetRasterBand(i + 1).WriteArray(lbl_vis[:, :, i])

        out_ds = None


def statistics_v0(image_dir, label_dir, class_tabel):
    """ 获得各区域影像数据的统计信息(由于不适合数据模式，暂时被淘汰了).
    Note: image_dir, label_dir are dir of all pairs of image and label,
        each pair of image and label should has same sign in file name.
        For example, 'tianmen_a.tiff' and 'tianmen_a_mask.tiff' both have 'tianmen_a' in their names .
    """
    # Image names list
    # img_names = sorted(os.listdir(image_dir))
    lbl_names = sorted(os.listdir(label_dir))

    # Execution operations
    # for (img_name, lbl_name) in tqdm(zip(img_names, lbl_names)):
    for lbl_name in lbl_names:
        print('\n' + '*' * 50 + '\n' + lbl_name.split('_mask')[0])

        # image = utils.raster2array(image_dir+'/'+img_name)
        label = raster2array(label_dir + '/' + lbl_name)
        # TODO： 一次性统计的话内存可能不够
        # assert image.shape[:2] == label.shape[:2]

        total_pixels = label.size
        for cls_name, ind in class_tabel.items():
            ratio = np.sum(label == ind) / total_pixels

            # Two way of print result:
            #   1. print sample ratio of each class vertically with markdown tabel style
            print('| %.2f%% |' % (ratio * 100))
            #   2. print them horizontally.
            # print('%.4fs, ' % ratio, end='')


def statistics(root, category):
    """ 根据GT_masks获得各区域影像数据的统计信息, 输出总体类别占比，以及各各区域内的类别占比.
    """
    import cv2

    class_num = category.num - 1  # 剔除BG
    regions = [name for name in os.listdir(root)]

    print('| Region num |', end='')
    for c in range(1, category.num):
        print(' %s |' % category.names[c], end='')

    total_pcpn = np.zeros((class_num), dtype=np.int64)  # Per class pixel num
    for reg in regions:
        lbl_list = filelist(root + '/' + reg, True, extension=['png', 'tif'])

        reg_pcpn = np.zeros((class_num), dtype=np.int64)  # Per class pixel num
        for lbl_path in lbl_list:
            lbl = cv2.imread(lbl_path, 0)

            for c in range(1, category.num):
                reg_pcpn[c-1] += np.sum(lbl == c)
        total_pcpn += reg_pcpn
        reg_ratios = reg_pcpn / np.sum(reg_pcpn)
        # 输出结果
        print('\n\r| %s |' % reg, end='')
        for c in range(1, category.num):
            print(' %.2f%% |' % (reg_ratios[c-1] * 100), end='')

    total_ratios = total_pcpn / np.sum(total_pcpn)
    print('\n\r| Total |', end='')
    for c in range(1, category.num):
        print(' %.2f%% |' % (total_ratios[c-1] * 100), end='')


def main():
    print('main')

    from category import category_C as mCategory

    ROOT = '/media/tao/Seagate Expansion Drive'
    # ROOT = r'D:\Data\GLC'
    GT_DIR = ROOT + '/' + 'mask_mid_up8'
    statistics(GT_DIR, mCategory)


if __name__ == "__main__":
    print('utils')
    # main()
    pass


# **************************************************
# *************** Abandoned func *******************
# **************************************************
def pixel2world(geoMatrix, col_row_st):
    """ Calculate the new geospatial coordinate by using
    gdal geomatrix (gdal.GetGeoTransform()) and pixel location in image.
    Returns:
        a tuple of geoTransform
    """
    col_start, row_start = col_row_st
    if type(geoMatrix) is tuple:
        geoMatrix = list(geoMatrix)  # tuple can't be copied
    new_geoMatrix = geoMatrix.copy()
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    # rtnX = geoMatrix[2]
    # rtnY = geoMatrix[4]
    # pixel = int((x - ulX) / xDist)
    # line = int((ulY - y) / yDist)
    new_geoMatrix[0] = ulX + col_start * xDist
    new_geoMatrix[3] = ulY + row_start * yDist
    return new_geoMatrix


def world2pixel(geoMatrix, xy):
    """ Calculate the pixel location in image by
    gdal geomatrix (gdal.GetGeoTransform()).

    Returns:
        (pixel, line) - (W, H)
    """
    x, y = xy
    ulx = geoMatrix[0]
    uly = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    # rtnX = geoMatrix[2]
    # rtnY = geoMatrix[4]
    pixel = round((x - ulx) / xDist)
    line = round((uly - y) / abs(yDist))

    return (pixel, line)


'''
class ReadRaster:
    def __init__(self, path,):
        self.ds = gdal.Open(path, gdal.GA_ReadOnly)
        self.rows = self.ds.RasterYSize  # 图像宽度
        self.cols = self.ds.RasterXSize  # 图像长度
        self.band_num = self.ds.RasterCount  # 波段数量
        self.proj = self.ds.GetProjection()  # 地图投影信息
        self.geotrans = self.ds.GetGeoTransform()  # 仿射矩阵

    def getRasterArray(self, bands=None):
        # Get array
        if self.band_num == 1:
            band = self.ds.GetRasterBand(1)
            array = band.ReadAsArray()  # [H, W]
        elif bands is None:
            array = self.ds.ReadAsArray()
            array = array.transpose((1, 2, 0))  # [H, W, num_bands]
        else:
            arrays = []
            for i in range(self.band_num):
                if i+1 in bands:
                    band = self.ds.GetRasterBand(i+1)
                    arrays.append(band.ReadAsArray())
            array = np.stack(arrays, axis=2)

        return array

    def getBandStatistics(self, bands=None, versbol=False):
        """ 计算波段统计量 输出为 min, max, Mean, stddev.
        """
        if bands is None:
            band_statis = np.zeros((self.band_num, 4))
            for i in range(self.band_num):
                data = self.ds.GetRasterBand(i + 1).GetStatistics(0, 1)
        else:
            band_statis = np.zeros((len(bands), 4))
            for i, b in enumerate(bands):
                data = self.ds.GetRasterBand(b).GetStatistics(0, 1)
                band_statis[i] = data
        if versbol:
            print(band_statis)
        return band_statis

    def writeArray(self,
                   savepath,
                   array,
                   geotransform=None,
                   geoprojection=None,
                   create_options=[]):
        array2raster(savepath, array, geotransform, geoprojection, create_options)
        return 'success'
'''
