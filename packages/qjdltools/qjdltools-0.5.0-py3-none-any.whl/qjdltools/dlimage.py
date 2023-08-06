'''
Tools collection of Data(np.ndarray) processing.

Note:
    1. cv2.imwrite(image_name, image, [1, 100]),
        [1, 100] mean set [cv2.IMWRITE_JPEG_QUALITY, 100]

Version 1.0  2018-04-03 15:44:13 by QiJi
Version 1.5  2018-04-07 22:34:53 by QiJi
Version 2.0  2018-10-25 16:59:23 by QiJi
'''

import os

import cv2
import numpy as np
from tqdm import tqdm

# from .dldata import get_label_info
from .fileop import filelist, rename_file


# **********************************************
# ************ Image basic tools ***************
# **********************************************
def randomcolor(band=3):
    values = [np.random.randint(0, 255) for i in range(3)]
    return tuple(values)


def convert_image_type(image_dir, new_type, old_type=None):
    '''Covert image's type(may be specify the old type).
    Args:
        new_type: The target type of image conversion(such as: 'png', 'jpg').
    '''
    image_names = filelist(image_dir, True, old_type)
    for name in tqdm(image_names):
        img = cv2.imread(name, 1)  # 默认BGR模式读，适应Tiff的标签图
        os.remove(name)
        name = os.path.splitext(name)[0]+'.'+new_type
        cv2.imwrite(name, img, [1, 100])


def one_hot_1(label, class_num):
    '''One hot code the label, not support RBG label.
    Args:
        label: a [HW] or [HW1] array
        class_num: num of classes
    Returns:
        one_hot: a 3D array of one_hot label (dtype=np.uint8), C=num of classes
    '''
    one_hot = np.zeros([label.shape[0], label.shape[1], class_num], dtype=np.uint8)
    for i in range(class_num):
        one_hot[:, :, i] = (label == i)  # TODO: need test [HW1]
    return one_hot


def one_hot_2(label, label_values):
    """
    One hot code the RBG label by replacing each pixel value with a vector of length num_classes
    Note: If class_dict is RGB, the label must be RGB(not BGR).
    Args:
        label: a [HWC] array, and C=3(be carefull about RGB or BGR)
        label_values: A list per class's color values.  [[0,0,0], [255,255,255], ]
    Returns:
        one_hot: one_hot label, C=num of classes
    """
    semantic_map = []
    for colour in label_values:
        equality = np.equal(label, colour)
        class_map = np.all(equality, axis=-1)
        semantic_map.append(class_map)
    semantic_map = np.stack(semantic_map, axis=-1).astype(np.uint8)

    return semantic_map


def one_hot_3(label, class_num):
    '''One hot code the label, classification result.
    Args:
        label: a [1] or [N1] array
        class_num: num of classes
    Returns:
        one_hot: a [NC] array of one_hot label, C=num of classes
    '''
    one_hot = np.zeros([label.shape[0], class_num], dtype=label.dtype)
    for i in range(class_num):
        one_hot[:, i] = (label == i)
    return one_hot


def class_label(label, label_values):
    '''
    Convert RGB label to 2D [HW] array, each pixel value is the classified class key.
    '''
    semantic_map = np.zeros(label.shape[:2], label.dtype)
    for i in range(len(label_values)):
        equality = np.equal(label, label_values[i])
        class_map = np.all(equality, axis=-1)
        semantic_map[class_map] = i
    return semantic_map


def reverse_one_hot(one_hot):
    '''Transform a 3D array in one-hot format (depth is num_classes),
    to a 2D array, each pixel value is the classified class key.
    '''
    return np.argmax(one_hot, axis=2)  # set axis=2 to limit the input is 3D


def colour_code_label(label, label_values, add_image=None, save_path=None):
    '''
    Given a [HW] array of class keys(or one hot[HWC]), colour code the label;
    also can weight the colour coded label and image, maybe save the final result.

    Args:
        label: single channel array where each value represents the class key.
        label_values: A list per class's color values. [[0,0,0], [255,255,255], ]
    Returns:
        Colour coded label or just save image return none.
    '''
    label, colour_codes = np.array(label), np.array(label_values)
    if len(label) == 3:
        label = np.argmax(label, axis=2)  # [HWC] -> [HW]
    color_label = colour_codes[label.astype(int)]  # TODO:此处直接uint8有错误
    color_label = color_label.astype(np.uint8)

    if add_image is not None:
        if add_image.shape != color_label.shape:
            cv2.resize(color_label, (add_image.shape[1], add_image.shape[0]),
                       interpolation=cv2.INTER_NEAREST)
        add_image = cv2.addWeighted(add_image, 0.7, color_label, 0.3, 0)
        if save_path is None:
            return color_label, add_image

    if save_path is not None:
        cv2.imwrite(save_path, color_label, [1, 100])
        if add_image is not None:
            cv2.imwrite(rename_file(save_path, addstr='mask'), add_image, [1, 100])
        return  # no need to return label if saved

    return color_label


def mask_img(image, label, mask_value=[0, 0, 0]):
    '''Mask image may with multi-bands with a specified value of label.
    Note: mask_value is value list.
    '''
    equality = np.equal(label, mask_value)
    mask = np.all(equality, axis=-1)
    image[mask] = [0, 0, 0]
    return image


# **********************************************
# ******** Common data Pre-treatment ***********
# **********************************************
def slide_crop(image, crop_params=[256, 256, 128], pad_mode=0, ifbatch=False):
    '''
    Slide crop image([HW] or [HWC] ndarray) into small piece,
    return list of sub_image or a [NHWC] array.

    Args:
        crop_params: [H, W, stride] (default=[256, 256, 128])

        pad_mode: One of the [-1, 0, 1] int values,
            -1 - Drop out the rest part;
            0 - Pad image at the end of W & H for fully cropping;
            1 - Pad image before and after W & H for fully cropping.
        ifbatch: Ture-return [NHWC] array; False-list of image.
    Return:
        size: [y, x]
            y - Num of images in the row direction.
            x - Num of images in the col direction.

    Carefully: If procided clipping parameters cannot completely crop the entire image,
        then it cannot be restored to original size during the recovery process.
    '''
    crop_h, crop_w, stride = crop_params
    H, W = image.shape[:2]

    if pad_mode < 0:
        # Adjust crop_params according to image_size
        crop_h = H if crop_h > H else crop_h
        crop_w = W if crop_w > W else crop_w

    h_res, w_res = (H-crop_h) % stride, (W-crop_w) % stride
    if h_res or w_res:  # Cannot completely slide-crop the target image
        sh = crop_h if H < crop_h else stride
        sw = crop_w if W < crop_w else stride
        # Adjust image_size according to crop_params
        if pad_mode >= 0:
            image, _ = pad_array(image, crop_h, crop_w, sh, sw, pad_mode)
        elif pad_mode == -1:
            if h_res:
                image = image[:-h_res, :]
            if w_res:
                image = image[:, :-w_res]
        H, W = image.shape[:2]  # Update image size

    image_list = []
    y = 0  # y:H(row)
    for i in range((H-crop_h)//stride + 1):
        x = 0  # x:W(col)
        for j in range((W-crop_w)//stride + 1):
            image_list.append(image[y:y+crop_h, x:x+crop_w].copy())
            x += stride
        y += stride
    size = [i+1, j+1]

    if ifbatch:
        batch_size = len(image_list)
        if batch_size == 1:
            return np.expand_dims(image_list[0], axis=0), size
        else:
            image_bantch = np.stack(image_list, axis=0)
            return image_bantch, size

    return image_list, size


def reverse_slide_crop(patches, crop_params, crop_info, HWC=True):
    '''
    Combine small patches by slide_crop into a big one.
    Args:
        patches: list of patches
        crop_params: [sub_h, sub_w, crop_stride]
        crop_info: [rows, cols]
            rows - Num of images in the row direction.
            cols - Num of images in the col direction.
    Returns:
        out_array: [HWC] or [CHW] ndarray.
    '''
    rows, cols = crop_info
    h, w, stride = crop_params
    # label = np.array(label)  # Tensor -> Array
    out_h, out_w = (rows-1)*stride+h, (cols-1)*stride+w
    if HWC:
        out_array = np.zeros([out_h, out_w, patches[0].shape[-1]], dtype=patches[0].dtype)  # [HWC]
    else:
        out_array = np.zeros([patches[0].shape[-1], out_h, out_w], dtype=patches[0].dtype)  # [HWC]
    y = 0  # y=h=row
    for i in range(rows):
        x = 0  # x=w=col
        for j in range(cols):
            if HWC:
                out_array[y:y+h, x:x+w] = patches[i*cols+j]
            else:
                out_array[:, y:y+h, x:x+w] = patches[i*cols+j]
            x += stride
        y += stride
    return out_array


def pad_array(array, kh, kw, sh, sw, mode=0):
    '''Pad array according kernel size and crop stride.

    Args:
        kh, kw: kernel height, kernel width.
        sh, sw: height directional stride, width directional stride.
        mode:
            0 - pad at the end of H/W dimension
            1 - pad at the begain and end of H/W dimension
    '''
    h, w = array.shape[:2]
    d = len(array.shape)
    pad_h, pad_w = sh - (h-kh) % sh, sw - (w-kw) % sw
    if mode == 0:
        pad_h, pad_w = (0, pad_h), (0, pad_w)
    elif mode == 1:
        pad_h = (pad_h//2, pad_h//2+1) if pad_h % 2 else (pad_h//2, pad_h//2)
        pad_w = (pad_w//2, pad_w//2+1) if pad_w % 2 else (pad_w//2, pad_w//2)
    pad_params = (pad_h, pad_w) if d == 2 else (pad_h, pad_w, (0, 0))
    return np.pad(array, pad_params, mode='constant'), pad_params


def scale_img(image, new_size=[256]):
    '''
    Scale the image (keep aspect ratio,
    let the shortest side equal to the target heigth/width,
    then crop it into the targe height and width).
    Args:
        new_size - a tuple may have only one element(H=W) or two elements(H, W).
    '''
    if len(new_size) == 2:
        H, W = new_size
        image = cv2.resize(image, (W, H))  # TODO: not support multi-bands
    elif len(new_size) == 1:
        h, w = image.shape[:2]
        if w > h:  # if image width > image height
            H, W = new_size[0], int(w*new_size[0]/h)
            st = int((W-H)/2)
            image = cv2.resize(image, (W, H))[:, st:st+H]
        else:  # if image height > image width
            H, W = int(w*new_size[0]/h), new_size[0]
            st = int((H-W)/2)
            image = cv2.resize(image, (W, H))[st:st+H, :]
    else:
        ValueError('Incorrect new_size!')

    return image


def resize_img(image, new_size=(256, 256), interpolation=cv2.INTER_LINEAR):
    """ Resize the image into new shape `new_size`, support multi-bands data.
    """
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]
        band_num = 1
    elif len(image.shape) == 3:
        band_num = image.shape[2]

    if band_num == 1 or band_num == 3:
        image = cv2.resize(image, new_size[::-1], interpolation=interpolation)
    else:
        new_image = np.zeros((new_size[0], new_size[1], band_num), dtype=image.dtype)
        for c in range(0, band_num):
            new_image[:, :, c] = cv2.resize(image[:, :, c], new_size[::-1],
                                            interpolation=interpolation)
        image = new_image

    return image


def unify_imgsize(img_dir, size=(256, 256), interpolation=cv2.INTER_NEAREST):
    '''
    Unify image size.
    Args:
        size: Uniform size(must be tuple)
        interpolation: Interpolation method of zoom image
    '''
    num = 1
    image_names = sorted(os.listdir(img_dir))
    for name in tqdm(image_names):
        img = cv2.imread(img_dir+'/'+name, -1)
        if img.shape[:2] != size:
            img = cv2.resize(img, size[::-1], interpolation)
        cv2.imwrite(img_dir+'/'+name, img, [1, 100])
        num += 1


# **********************************************
# ************ Main functions ******************
# **********************************************
def crop_imgs(image_dir, out_dir=None, crop_params=None, ifPad=True):
    ''' Slide crop images into small piece and save them. '''
    if out_dir is None:
        out_dir = image_dir

    image_names = sorted(os.listdir(image_dir))
    for name in tqdm(image_names):
        image = cv2.imread(image_dir+'/'+name, -1)
        # 附加操作
        # h, w = image.shape[:2]
        # image = cv2.resize(image, (int(w*0.7), int(h*0.7)))
        imgs, _ = slide_crop(image, crop_params, ifPad)
        num = len(imgs)
        for i in range(num):
            save_name = rename_file(name, addstr="_%d" % (i+1))  # TODO: 子图编号的位数
            cv2.imwrite(out_dir+'/'+save_name, imgs[i], [1, 100])


if __name__ == '__main__':
    # main()
    # main_of_imgAndlabel_ops()
    # in_dir = '/home/tao/Code/Result/CVPR/测试集_真实/val_labels_visual'
    # in_dir = 'D:/Data_Lib/Other/Small/6/train_labels'
    # out_dir = '/home/tao/Code/Result/CVPR/测试集_真实/val_labels'
    # in_dir = '/home/tao/Data/RBDD/BackUp/Orignal_data/val_labels'
    # out_dir = '/home/tao/Data/RBDD/512/val_labels'
    # main_of_img_ops(in_dir, out_dir)
    # crop_imgs(in_dir, out_dir, [512, 512, 512])

    pass
