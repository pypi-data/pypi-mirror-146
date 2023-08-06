# -*- coding:utf-8 -*-
'''
Some old, useless function.
'''
import os
import sys
import datetime
import cv2
from PIL import Image
import math
# import h5py
import torch
import numpy as np
from tqdm import tqdm
from skimage import morphology
import torchvision.transforms as ttransform

from .fileop import filelist
from .dltrain import fast_hist, runingScore
from .dlimage import resize_img




def get_label_info(file_path):
    """
    Retrieve the class names and label values for the selected dataset.
    Must be in CSV or Txt format!

    Args:
        file_path: The file path of the class dictionairy

    Returns:
        class_names: A list of class names.
        label values: A list per class's color values. [[0,0,0], [255,255,255], ]
    """
    import csv
    filename, exten = os.path.splitext(file_path)
    if not (exten == ".csv" or exten == ".txt"):
        return ValueError("File is not a CSV or TxT!")

    class_names, label_values = [], []
    with open(file_path, 'r') as f:
        file_reader = csv.reader(f, delimiter=',')
        row = next(file_reader)  # skip one line
        for row in file_reader:
            if row != []:
                class_names.append(row[0])
                label_values.append([int(row[1]), int(row[2]), int(row[3])])
    return class_names, label_values


def train_log(X, prefix='', f=None):
    """ Print with time. To console or a file(f) """
    time_stamp = datetime.datetime.now().strftime("[%d %H:%M:%S]")
    if f is not None:
        if type(f) == str:
            with open(f, 'a') as f:
                f.write(time_stamp + " " + X)
        else:
            f.write(time_stamp + " " + X)

    sys.stdout.write(prefix + time_stamp + " " + X)
    sys.stdout.flush()


# **********************************************
# ********** Commen data augment ***************
# **********************************************
def filp_array(array, flipCode):
    '''Filp an [HW] or [HWC] array vertically or horizontal according to flipCode.'''
    if flipCode != -1:
        array = np.flip(array, flipCode)
    elif flipCode == -1:
        array = np.flipud(array)
        array = np.fliplr(array)
    return array


def resized_crop(image, i, j, h, w, size, interpolation=cv2.INTER_LINEAR):
    '''Crop the given ndarray image and resize it to desired size.
    Args:
        i: Upper pixel coordinate.
        j: Left pixel coordinate.
        h: Height of the cropped image.
        w: Width of the cropped image.
        size: (Height, Width) must be tuple
    '''
    h_org, w_org = image.shape[:2]
    i, j = max(0, i), max(0, j)
    h, w = min(h_org-i, h), min(w_org-j, w)
    image = image[i:i+h, j:j+w]

    image = resize_img(image, new_size=size, interpolation=interpolation)
    return image


def center_crop(array, crop_hw=(256, 256)):
    ''' Crops the given image(label) at the center.
    '''
    h, w = array.shape[:2]
    th, tw = crop_hw
    th, tw = min(h, th), min(w, tw)

    i = int(round((h - th) / 2.))
    j = int(round((w - tw) / 2.))

    array = array[i:i+th, j:j+tw]
    return array


def random_crop(array, crop_hw=(256, 256)):
    '''
    Crop image(label) randomly
    '''
    crop_h, crop_w = crop_hw
    if (crop_h < array.shape[0] and crop_w < array.shape[1]):
        x = np.random.randint(0, array.shape[0] - crop_h)  # row
        y = np.random.randint(0, array.shape[1] - crop_w)  # column
        return array[x:x + crop_h, y:y + crop_w]

    elif (crop_h == array.shape[0] and crop_w == array.shape[1]):
        return array

    else:
        raise Exception('Crop size > image.shape')


def random_crop_pair(image, label, crop_hw=(256, 256)):
    '''
    Crop image and label randomly

    '''
    crop_h, crop_w = crop_hw
    if image.shape[:2] != label.shape[:2]:
        raise Exception('Image and label must have the same shape')
    if (crop_h < image.shape[0] and crop_w < image.shape[1]):
        x = np.random.randint(0, image.shape[0] - crop_h)  # row
        y = np.random.randint(0, image.shape[1] - crop_w)  # column
        # label maybe multi-channel[H,W,C] or one-channel [H,W]
        return image[x:x + crop_h, y:y + crop_w], label[
            x:x + crop_h, y:y + crop_w]
    elif (crop_h == image.shape[0] and crop_w == image.shape[1]):
        return image, label
    else:
        raise Exception('Crop size > image.shape')


def random_crop_balance(image, label, crop_hw=(256, 256), num_classes=0):
    '''
    Crop image(label) randomly for serval times(now four times most),
    and return the one in which per class RATIO most balancing.
    Don't support RGB label now.
    Args:
        label: 1. [HW]; 2. [HW1]; 3. one_hot-[HWC]; 4. rgb-[HWC]-目前不支持rbg!!!
            Note: 1&2 class_num need to be specified!!!
        num_classes: default=0, only one_hot label don't have to specify.
    Returns:
        image: croped image
        label: croped laebl
    '''
    crop_h, crop_w = crop_hw
    if (image.shape[0] != label.shape[0]) or (image.shape[1] != label.shape[1]):
        raise Exception('Image and label must have the same dimensions!')

    if (crop_w < image.shape[1]) and (crop_h < image.shape[0]):
        x, y = [0, 0, 0, 0], [0, 0, 0, 0]
        rate = [1., 1., 1., 1.]  # store min RATIO
        sum_area = crop_h * crop_w

        if len(label.shape) == 2 or label.shape[-1] == 1:  # [HW] or [HW1]
            for i in range(4):  # try four times and choose the max rate's x,y
                x[i] = np.random.randint(0, image.shape[1] - crop_w)  # W
                y[i] = np.random.randint(0, image.shape[0] - crop_h)  # H
                tmp_label = label[y[i]:y[i] + crop_h, x[i]:x[i] + crop_w].crop()

                for j in range(num_classes):
                    indArr = [tmp_label == j]
                    tmp_rate = np.sum(indArr) / sum_area
                    if tmp_rate == 0:
                        rate[i] = tmp_rate
                        break
                    elif tmp_rate < rate[i]:
                        rate[i] = tmp_rate

        else:  # [HWC] - only support one_hot label now
            for i in range(4):
                x[i] = np.random.randint(0, image.shape[1] - crop_w)  # W
                y[i] = np.random.randint(0, image.shape[0] - crop_h)  # H
                tmp_label = label[y[i]:y[i] + crop_h, x[i]:x[i] + crop_w, :].crop()

                # For one_hot label
                for j in range(tmp_label.shape[2]):  # traverse all channel-class
                    indArr = tmp_label[:, :, j]
                    tmp_rate = np.sum(indArr) / sum_area
                    if tmp_rate == 0:
                        rate[i] = tmp_rate
                        break
                    elif tmp_rate < rate[i]:
                        rate[i] = tmp_rate

        ind = rate.index(max(rate))  # choose the max RATIO area
        x, y = x[ind], y[ind]

        label = label[y:y + crop_h, x:x + crop_w]
        image = image[y:y + crop_h, x:x + crop_w]
        return image, label

    elif (crop_w == image.shape[1] and crop_h == image.shape[0]):
        return image, label

    else:
        raise Exception('Crop shape exceeds image dimensions!')


def randomShiftScaleRotate(image,
                           mask=None,
                           shift_limit=(-0.0, 0.0),
                           scale_limit=(-0.0, 0.0),
                           rotate_limit=(-0.0, 0.0),
                           aspect_limit=(-0.0, 0.0),
                           borderMode=cv2.BORDER_CONSTANT,
                           p=0.5):
    """
    Random shift scale rotate image (support multi-band) may be with mask.

    Args:
        p (float): Probability of rotation.
    """
    if np.random.random() < p:
        if len(image.shape) > 2:
            height, width, channel = image.shape
        else:
            (height, width), channel = image.shape, 1

        angle = np.random.uniform(rotate_limit[0], rotate_limit[1])
        scale = np.random.uniform(1 + scale_limit[0], 1 + scale_limit[1])
        aspect = np.random.uniform(1 + aspect_limit[0], 1 + aspect_limit[1])
        sx = scale * aspect / (aspect**0.5)
        sy = scale / (aspect**0.5)
        dx = round(np.random.uniform(shift_limit[0], shift_limit[1]) * width)
        dy = round(np.random.uniform(shift_limit[0], shift_limit[1]) * height)

        cc = np.math.cos(angle / 180 * np.math.pi) * sx
        ss = np.math.sin(angle / 180 * np.math.pi) * sy
        rotate_matrix = np.array([[cc, -ss], [ss, cc]])

        box0 = np.array([
            [0, 0],
            [width, 0],
            [width, height],
            [0, height],
        ])
        box1 = box0 - np.array([width / 2, height / 2])
        box1 = np.dot(box1, rotate_matrix.T) + np.array(
            [width / 2 + dx, height / 2 + dy])

        box0 = box0.astype(np.float32)
        box1 = box1.astype(np.float32)
        mat = cv2.getPerspectiveTransform(box0, box1)

        if channel > 3:
            for c in range(channel):
                band = image[:, :, c]
                image[:, :, c] = cv2.warpPerspective(
                    band, mat, (width, height),
                    flags=cv2.INTER_LINEAR, borderMode=borderMode)
        else:
            image = cv2.warpPerspective(
                image, mat, (width, height),
                flags=cv2.INTER_LINEAR, borderMode=borderMode)
        if mask is not None:
            mask = cv2.warpPerspective(
                mask, mat, (width, height),
                flags=cv2.INTER_LINEAR, borderMode=borderMode)
    if mask is not None:
        return image, mask
    else:
        return image


def rotate_pair_img(xb, yb, angle):
    '''rotate xb, yb'''
    h, w = xb.shape[0], xb.shape[1]
    M_rotate = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1)
    xb = cv2.warpAffine(xb, M_rotate, (w, h))
    yb = cv2.warpAffine(yb, M_rotate, (w, h))
    return xb, yb


def randomHueSaturationValue(image,
                             hue_shift_limit=(-180, 180),
                             sat_shift_limit=(-255, 255),
                             val_shift_limit=(-255, 255),
                             u=0.5):
    if np.random.random() < u:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(image)
        hue_shift = np.random.randint(hue_shift_limit[0],
                                      hue_shift_limit[1] + 1)
        hue_shift = np.uint8(hue_shift)
        h += hue_shift
        sat_shift = np.random.uniform(sat_shift_limit[0], sat_shift_limit[1])
        s = cv2.add(s, sat_shift)
        val_shift = np.random.uniform(val_shift_limit[0], val_shift_limit[1])
        v = cv2.add(v, val_shift)
        image = cv2.merge((h, s, v))
        #image = cv2.merge((s, v))
        image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)

    return image


def randomColorAugment(image, brightness=0.1, contrast=0.1):
    ''' Randomly jotter the brightness and contrast of each band in ndarray imagery.
    '''
    if brightness > 0:
        brightness_factor = np.random.uniform(max(0, 1-brightness), 1+brightness)
        if brightness_factor > 1:
            alpha = brightness_factor - 1
            degenerate = np.ones_like(image) * 255
        elif brightness_factor <= 1:
            alpha = 1 - brightness_factor
            degenerate = np.zeros_like(image)
        image = cv2.addWeighted(degenerate, alpha, image, (1-alpha), 0)

    # Adjust contrast, saturation and hue reference: https://zhuanlan.zhihu.com/p/24425116
    if contrast > 0:
        contrast_factor = np.random.uniform(max(0, 1-contrast), 1+contrast)
        image = np.clip(image * contrast_factor, 0, 255).astype(np.uint8)
    return image


def random_noise(image, mode='gaussian', seed=None, clip=True, **kwargs):
    """
    Function to add random noise of various types to a image.

    Parameters
    ----------
    image : ndarray
        Input image data sized of [HW] or [HWC] (support multi-band), from range of (0~255).
    mode : str, optional
        One of the following strings, selecting the type of noise to add:

        - 'gaussian'  Gaussian-distributed additive noise.
        - 'localvar'  Gaussian-distributed additive noise, with specified
                      local variance at each point of `image`.
        - 'poisson'   Poisson-distributed noise generated from the data.
        - 'salt'      Replaces random pixels with 1.
        - 'pepper'    Replaces random pixels with 0 (for unsigned images) or
                      -1 (for signed images).
        - 's&p'       Replaces random pixels with either 1 or `low_val`, where
                      `low_val` is 0 for unsigned images or -1 for signed
                      images.
        - 'speckle'   Multiplicative noise using out = image + n*image, where
                      n is uniform noise with specified mean & variance.
    seed : int, optional
        If provided, this will set the random seed before generating noise,
        for valid pseudo-random comparisons.
    clip : bool, optional
        If True (default), the output will be clipped after noise applied
        for modes `'speckle'`, `'poisson'`, and `'gaussian'`. This is
        needed to maintain the proper image data range. If False, clipping
        is not applied, and the output may extend beyond the range [0, 255].
    mean : float, optional
        Mean of random distribution. Used in 'gaussian' and 'speckle'.
        Default : 0.
    var : float, optional
        Variance of random distribution. Used in 'gaussian' and 'speckle'.
        Note: variance = (standard deviation) ** 2. Default : 0.01
    local_vars : ndarray, optional
        Array of positive floats, same shape as `image`, defining the local
        variance at every image point. Used in 'localvar'.
    amount : float, optional
        Proportion of image pixels to replace with noise on range [0, 1].
        Used in 'salt', 'pepper', and 'salt & pepper'. Default : 0.01
    salt_vs_pepper : float, optional
        Proportion of salt vs. pepper noise for 's&p' on range [0, 1].
        Higher values represent more salt. Default : 0.5 (equal amounts)

    Returns
    -------
    out : ndarray
        Output floating-point image data on range [0, 255].

    Notes
    -----
    Speckle, Poisson, Localvar, and Gaussian noise may generate noise outside
    the valid image range. The default is to clip (not alias) these values,
    but they may be preserved by setting `clip=False`. Note that in this case
    the output may contain values outside the ranges [0, 255].
    Use this option with care.

    Because of the prevalence of exclusively positive floating-point images in
    intermediate calculations, it is not possible to intuit if an input is
    signed based on dtype alone. Instead, negative values are explicitly
    searched for. Only if found does this function assume signed input.
    Unexpected results only occur in rare, poorly exposes cases (e.g. if all
    values are above 50 percent gray in a signed `image`). In this event,
    manually scaling the input to the positive domain will solve the problem.

    The Poisson distribution is only defined for positive integers. To apply
    this noise type, the number of unique values in the image is found and
    the next round power of two is used to scale up the floating-point result,
    after which it is scaled back down to the floating-point image range.

    To generate Poisson noise against a signed image, the signed image is
    temporarily converted to an unsigned image in the floating point domain,
    Poisson noise is generated, then it is returned to the original range.

    """
    mode = mode.lower()

    if seed is not None:
        np.random.seed(seed=seed)

    allowedtypes = {
        'gaussian': 'gaussian_values',
        'localvar': 'localvar_values',
        'poisson': 'poisson_values',
        'salt': 'sp_values',
        'pepper': 'sp_values',
        's&p': 's&p_values',
        'speckle': 'gaussian_values'}

    kwdefaults = {
        'mean': 0.,
        'var': 0.01,
        'amount': 0.01,
        'salt_vs_pepper': 0.5,
        'local_vars': np.zeros_like(image) + 0.01}

    allowedkwargs = {
        'gaussian_values': ['mean', 'var'],
        'localvar_values': ['local_vars'],
        'sp_values': ['amount'],
        's&p_values': ['amount', 'salt_vs_pepper'],
        'poisson_values': []}

    for key in kwargs:
        if key not in allowedkwargs[allowedtypes[mode]]:
            raise ValueError('%s keyword not in allowed keywords %s' %
                             (key, allowedkwargs[allowedtypes[mode]]))

    # Set kwarg defaults
    for kw in allowedkwargs[allowedtypes[mode]]:
        kwargs.setdefault(kw, kwdefaults[kw])

    img_type = image.dtype
    if mode == 'gaussian':
        noise = np.random.normal(kwargs['mean'], kwargs['var'] ** 0.5,
                                 image.shape)
        out = image + (noise*128).astype(img_type)

    elif mode == 'localvar':
        # Ensure local variance input is correct
        if (kwargs['local_vars'] <= 0).any():
            raise ValueError('All values of `local_vars` must be > 0.')

        # Safe shortcut usage broadcasts kwargs['local_vars'] as a ufunc
        noise = np.random.normal(0, kwargs['local_vars'] ** 0.5)
        out = image + (noise * 128).astype(img_type)

    elif mode == 'poisson':
        # Determine unique values in image & calculate the next power of two
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))

        # Generating noise for each unique value in image.
        out = (np.random.poisson(image * vals) / float(vals)).astype(img_type)

    elif mode == 'salt':
        # Re-call function with mode='s&p' and p=1 (all salt noise)
        out = random_noise(image, mode='s&p', seed=seed,
                           amount=kwargs['amount'], salt_vs_pepper=1.)

    elif mode == 'pepper':
        # Re-call function with mode='s&p' and p=1 (all pepper noise)
        out = random_noise(image, mode='s&p', seed=seed,
                           amount=kwargs['amount'], salt_vs_pepper=0.)

    elif mode == 's&p':
        out = image.copy()
        p = kwargs['amount']
        q = kwargs['salt_vs_pepper']
        flipped = np.random.choice([True, False], size=image.shape,
                                   p=[p, 1 - p])
        salted = np.random.choice([True, False], size=image.shape,
                                  p=[q, 1 - q])
        peppered = ~salted
        out[flipped & salted] = 255
        out[flipped & peppered] = 0

    elif mode == 'speckle':
        noise = np.random.normal(kwargs['mean'], kwargs['var'] ** 0.5,
                                 image.shape)
        out = image + (image * noise).astype(img_type)

    # Clip back to original range, if necessary
    if clip:
        out = np.clip(out, 0, 255)

    return out


def blur(image, ksize=3):
    if len(image.shape) > 2:
        for c in range(image.shape[2]):
            band = image[:, :, c]
            image[:, :, c] = cv2.blur(band, (ksize, ksize))
    else:
        image = cv2.blur(image, (ksize, ksize))
    return image


def gamma_transform(img, gamma):
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img, gamma_table)


def random_gamma_transform(img, gamma_vari):
    log_gamma_vari = np.log(gamma_vari)
    alpha = np.random.uniform(-log_gamma_vari, log_gamma_vari)
    gamma = np.exp(alpha)
    return gamma_transform(img, gamma)


# **********************************************
# ************** LR Schedler *******************
# **********************************************
def adjust_learning_rate(optimizer, cepoch, args, lr=None):
    """Decay the learning rate based on schedule"""
    lr = args.lr if lr is None else lr

    def _cal_coefficient(epoch):
        if epoch < args.warmup:
            coefficient = (epoch + 1) / args.warmup  # warmup
        else:
            if args.lr_policy == 'cosine':  # cosine lr schedule
                coefficient = 0.5 * (1. + math.cos(math.pi * epoch / args.mepoch))
            elif args.lr_policy == 'linear':
                coefficient = 1 - (epoch-args.warmup) / (args.mepoch-args.warmup)
            elif args.lr_policy == 'step':  # stepwise lr schedule
                for milestone in args.milestones:
                    coefficient = args.lr_decay[1] if epoch >= milestone else 1.
            elif args.lr_policy == 'polyline':  # stepwise lr schedule
                if epoch > args.milestones[0]:
                    # start decay
                    coefficient = (args.mepoch - epoch)/(args.mepoch - args.milestones[0])
        return coefficient

    last_epoch = max(1, cepoch-1)
    last_coeff = _cal_coefficient(last_epoch)
    cur_coeff = _cal_coefficient(cepoch)
    for param_group in optimizer.param_groups:
        base_lr = param_group['lr'] / last_coeff
        new_lr = base_lr * cur_coeff
        param_group['lr'] = new_lr

    return lr * cur_coeff  # main base lr (no hos)


# **********************************************
# ******** Common data Pre-treatment ***********
# **********************************************
def label_pretreat(label_dir, label_values):
    '''
    Pre-treat the orignal RGB label, to fix the apparent bug.
    (Actually it eliminate the wrong colors that are not in class_dict)
    By the way, unify the dtype of label imgs to png.
    '''
    l_names = filelist(label_dir, ifPath=True)
    for name in tqdm(l_names):
        label = cv2.imread(name, 1)  # read in RGB
        os.remove(name)
        name = os.path.splitext(name)[0] + '.png'
        new_label = np.zeros(label.shape, label.dtype)
        # Fix the color(stand for a class) by class-info
        for color in label_values:
            equality = np.equal(label, color)
            ind_mat = np.all(equality, axis=-1)
            new_label[ind_mat] = color  # this color list can be customized
        cv2.imwrite(name, new_label)  # new_label-BGR(according to class_dict)


# **********************************************
# *************** Evaluation *******************
# **********************************************
class RoadExtractionScore(runingScore):
    """Accuracy evaluation for road extraction.
    Only two class: 0-bg, 1-road.
    """

    def update(self, y_true, y_pred):
        """Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix. """
        hist = fast_hist(y_true, y_pred, self.n_classes)
        self.confusion_matrix += hist
        return self.get_scores(hist)

    def add(self, y_true, y_pred):
        """Add a new pair of predicted label and GT label,
        update the confusion_matrix. """
        hist = fast_hist(y_true, y_pred, self.n_classes)
        self.confusion_matrix += hist

    def get_scores(self, hist=None):
        """Returns accuracy score evaluation result.
            - 1. Precision{ TP / (TP+FP) }
            - 2. Recall{ TP / (TP+FN) }
            - 3. F1score
            - 4. Class IoU
            - 5. Mean IoU
            - 6. FreqW Acc
        """
        hist = self.confusion_matrix if hist is None else hist

        # Take class 1-road as postive class:
        TP = hist[1, 1]  # Ture Positive(road pixels are classified into road class)
        FN = hist[1, 0]  # False Negative(road pixels are classified into bg class)
        FP = hist[0, 1]  # False Positive(bg pixels are classified into road class)
        # TN = hist[0, 0]  # Ture Negative(bg pixels are classified into bg class)

        prec = TP / (TP + FP + 1e-8)  # Precision
        rec = TP / (TP + FN + 1e-8)  # Recall
        F1 = 2*TP / (2*TP + FP + FN + 1e-8)  # F1 Score

        # IoU (tested)
        cls_iu = np.diag(hist) / (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist))
        mean_iu = np.nanmean(cls_iu)
        # Frequency Weighted IoU(FWIoU) 根据每个类出现的频率为其设置权重
        freq = hist.sum(axis=1) / (hist.sum()+1e-8)
        fwavacc = (freq[freq > 0] * cls_iu[freq > 0]).sum()
        # cls_iu = dict(zip(range(self.n_classes), iu))

        return (
            {
                'Precision': prec,
                'Recall': rec,
                'F1score': F1,
                'Class IoU': cls_iu,
                'Mean IoU': mean_iu,
                'FreqW Acc': fwavacc,
            }  # Return as a dictionary
        )

    def keys(self):
        score_keys = [
            'Precision,Recall,F1score,Class IoU,Class IoU,Mean IoU,FreqW Acc'
        ]  # note 'Class IoU'
        return score_keys


class RelaxedRoadExtractionScore(runingScore):
    """Relax Accuracy evaluation for road extraction.
    Only two class: 0-bg, 1-road.
    """
    def __init__(self, rho=1):
        self.rho = rho*2 + 1
        self.confusion_matrix_p = np.zeros((2, 2), np.int64)  # For relaxed precision
        self.confusion_matrix_r = np.zeros((2, 2), np.int64)  # For relaxed recall

    def update(self, y_true, y_pred):
        """Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix."""
        if self.rho > 1:
            selem = morphology.square(self.rho, dtype=y_true.dtype)
            tp_label_true = morphology.dilation(y_true, selem)
            tp_label_pred = morphology.binary_dilation(y_pred, selem)
            hist1 = fast_hist(tp_label_true, y_pred, 2)
            hist2 = fast_hist(y_true, tp_label_pred, 2)
        else:
            hist = fast_hist(y_true, y_pred, 2)
            hist1, hist2 = hist, hist

        self.confusion_matrix_p += hist1
        self.confusion_matrix_r += hist2
        return self.get_scores(hist1, hist2)

    def add(self, y_true, y_pred):
        """ Add new pairs of predicted label and GT label to update the confusion_matrix. """
        if self.rho > 0:
            selem = morphology.square(self.rho, dtype=np.int64)
            tp_lt = morphology.binary_dilation(y_true, selem)
            tp_lp = morphology.binary_dilation(y_pred, selem)
            self.confusion_matrix_p += fast_hist(tp_lt, y_pred, 2)
            self.confusion_matrix_r += fast_hist(y_true, tp_lp, 2)
        else:
            hist = fast_hist(y_true, y_pred, 2)
            self.confusion_matrix_p += hist
            self.confusion_matrix_r += hist

    def get_scores(self, hist_p=None, hist_r=None):
        hist_p = self.confusion_matrix_p if hist_p is None else hist_p
        hist_r = self.confusion_matrix_r if hist_r is None else hist_r

        prec = hist_p[1, 1] / (hist_p[1, 1] + hist_p[0, 1] + 1e-8)  # Precision
        rec = hist_r[1, 1] / (hist_r[1, 1] + hist_r[1, 0] + 1e-8)  # Recall
        f1 = 2 * prec * rec / (prec + rec + 1e-8)
        return (
            {
                "Precision": prec,
                "Recall": rec,
                "F1score": f1
            }  # Return as a dictionary
        )

    def reset(self):
        """ Reset confusion_matrixs. """
        self.confusion_matrix_p = np.zeros((2, 2), dtype=np.int64)
        self.confusion_matrix_r = np.zeros((2, 2), dtype=np.int64)


# **********************************************
# **************** Transform *******************
# **********************************************
class Resize(object):
    """
    Resize image (maybe with mask).

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        insize (tuple): (h, w) of image (mask)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, insize, mode='cls'):
        self.mode = mode
        self.insize = insize

        if self.mode == 'cls':
            self.transform = self.single_resize
        elif self.mode == 'seg':
            self.transform = self.join_resize

    def single_resize(self, sample):
        image = sample['image']
        if image.shape[:2] == self.insize:
            return sample

        sample['image'] = resize_img(image, self.insize, cv2.INTER_LINEAR)
        return sample

    def join_resize(self, sample):
        image, mask = sample['image'], sample['label']
        if image.shape[:2] == self.insize:
            return sample

        h, w = self.insize

        image = resize_img(image, self.insize, cv2.INTER_LINEAR)
        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
        sample['image'], sample['label'] = image, mask
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class RandomCrop(object):
    """
    Random crop image (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        insize (tuple): (h, w) of image (mask)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, insize, mode='cls'):
        self.mode = mode
        self.insize = insize

        if self.mode == 'cls':
            self.transform = self.random_crop

        elif self.mode == 'seg':
            self.transform = self.random_crop_pair

    def random_crop(self, sample):
        image = sample['image']
        if (image.shape[0] > self.insize[0]) and (image.shape[1] > self.insize[1]):
            image = random_crop(image, self.insize)
        sample['image'] = image
        return sample

    def random_crop_pair(self, sample):
        image, mask = sample['image'], sample['label']
        image, mask = random_crop_pair(image, mask, self.insize)
        sample['image'], sample['label'] = image, mask
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class CenterCrop(object):
    """
    Center crop image (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        insize (tuple): (h, w) of image (mask)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, insize, mode='cls'):
        self.mode = mode
        self.insize = insize

        if self.mode == 'cls':
            self.transform = self.center_crop

        elif self.mode == 'seg':
            self.transform = self.center_crop_pair

    def center_crop(self, sample):
        image = sample['image']
        if (image.shape[0] > self.insize[0]) and (image.shape[1] > self.insize[1]):
            image = center_crop(image, self.insize)
        sample['image'] = image
        return sample

    def center_crop_pair(self, sample):
        image, mask = sample['image'], sample['label']
        image = center_crop(image, self.insize)
        mask = center_crop(mask, self.insize)
        sample['image'], sample['label'] = image, mask
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class RandomScaleAspctCrop(object):
    """
    Random crop image (maybe with mask).

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        insize (tuple): (h, w) of image (mask)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, insize, scale=(0.25, 0.75), ratio=(3./4., 4./3.), p=0.5, mode='cls'):
        self.mode = mode
        self.insize = insize
        self.scale = scale
        self.ratio = ratio
        self.p = p

        if self.mode == 'cls':
            self.transform = self.random_scale_aspct_crop

        elif self.mode == 'seg':
            self.transform = self.join_random_scale_aspct_crop

    def random_scale_aspct_crop(self, sample):
        image = sample['image']
        if image.shape[0] < self.insize[0]:
            image = resize_img(image, self.insize)

        H, W = image.shape[:2]  # ori_height, ori_width
        area = H*W
        if np.random.random() < self.p:
            for attempt in range(5):
                target_area = np.random.uniform(*self.scale) * area
                aspect_ratio = np.random.uniform(*self.ratio)

                w = int(round(np.sqrt(target_area * aspect_ratio)))
                h = int(round(np.sqrt(target_area / aspect_ratio)))

                if np.random.random() < 0.5:
                    w, h = h, w

                if w < W and h < H:
                    i = np.random.randint(0, H - h)  # crop start point(row/y)
                    j = np.random.randint(0, W - w)  # crop start point(col/x)
                    sample['image'] = resized_crop(
                        image, i, j, h, w, self.insize, cv2.INTER_LINEAR)
                    return sample
        else:
            w, h = W, H
        # Fallback
        w, h = min(w, W), min(h, H)
        i, j = (H - w) // 2, (W - w) // 2
        sample['image'] = resized_crop(
            image, i, j, h, w, self.insize, cv2.INTER_LINEAR)
        return sample

    def join_random_scale_aspct_crop(self, sample):
        image, mask = sample['image'], sample['label']

        H, W = image.shape[:2]  # ori_height, ori_width
        area = H*W
        if np.random.random() < self.p:
            for attempt in range(3):
                target_area = np.random.uniform(*self.scale) * area
                aspect_ratio = np.random.uniform(*self.ratio)

                w = int(round(np.sqrt(target_area * aspect_ratio)))
                h = int(round(np.sqrt(target_area / aspect_ratio)))

                if np.random.random() < 0.5:
                    w, h = h, w

                if w < W and h < H:
                    i = np.random.randint(0, H - h)  # crop start point(row/y)
                    j = np.random.randint(0, W - w)  # crop start point(col/x)
                    sample['image'] = resized_crop(
                        image, i, j, h, w, self.insize, cv2.INTER_LINEAR)
                    sample['label'] = resized_crop(
                        mask, i, j, h, w, self.insize, cv2.INTER_NEAREST)
                    return sample
        else:
            w, h = W, H
        # Fallback
        w, h = min(w, W), min(h, H)
        i, j = (H - w) // 2, (W - w) // 2
        sample['image'] = resized_crop(
            image, i, j, h, w, self.insize, cv2.INTER_LINEAR)
        sample['label'] = resized_crop(
            mask, i, j, h, w, self.insize, cv2.INTER_NEAREST)
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class SpaceAugment(object):
    """
    Space data augmentations for image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self,
                 shift_limit=(-0.0, 0.0),
                 scale_limit=(-0.0, 0.0),
                 rotate_limit=(-0.0, 0.0),
                 aspect_limit=(-0.0, 0.0),
                 rot=True,
                 flip=True,
                 p=0.5,
                 mode='cls'):
        self.mode = mode
        self.shift_limit = shift_limit
        self.scale_limit = scale_limit
        self.rotate_limit = rotate_limit
        self.aspect_limit = aspect_limit
        self.if_rot = rot
        self.if_flip = flip
        self.p = p

        if self.mode == 'cls':
            self.transform = self.single_transform
        elif self.mode == 'seg':
            self.transform = self.join_transform

    def join_transform(self, sample):
        image, mask = sample['image'], sample['label']

        # Join Random Filp
        if self.if_flip:
            f = [1, 0, -1, 2, 2][np.random.randint(0, 5)]  # [1, 0, -1, 2, 2]
            if f != 2:
                image, mask = filp_array(image, f), filp_array(mask, f)

        # Join Random Roate (Only 0, 90, 180, 270)
        if self.if_rot:
            k = np.random.randint(0, 4)  # [0, 1, 2, 3]
            image = np.rot90(image, k, (1, 0))  # clockwise
            mask = np.rot90(mask, k, (1, 0))

        # Affine transformation
        image, mask = randomShiftScaleRotate(
            image, mask,
            shift_limit=self.shift_limit, scale_limit=self.scale_limit,
            rotate_limit=self.rotate_limit, aspect_limit=self.aspect_limit,
            # borderMode=cv2.BORDER_REFLECT,
            p=self.p)

        sample['image'], sample['label'] = image.copy(), mask.copy()
        return sample

    def single_transform(self, sample):
        image = sample['image']

        # Join Random Filp
        if self.if_flip:
            f = [1, 0, -1, 2, 2][np.random.randint(0, 5)]  # [1, 0, -1, 2, 2]
            if f != 2:
                image = filp_array(image, f)

        # Random Roate (Only 0, 90, 180, 270)
        if self.if_rot:
            k = np.random.randint(0, 4)  # [0, 1, 2, 3]
            image = np.rot90(image, k, (1, 0))  # clockwise

        # Affine transformation
        image = randomShiftScaleRotate(
            image,
            shift_limit=self.shift_limit, scale_limit=self.scale_limit,
            rotate_limit=self.rotate_limit, aspect_limit=self.aspect_limit,
            # borderMode=cv2.BORDER_REFLECT,
            p=self.p)

        sample['image'] = image.copy()
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class RandomRotateAndFlip(object):
    """
    Random rotate for image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        mode: 'seg'-segmentation; 'cls'-classification
    """
    def __init__(self, p=0.5, mode='cls'):
        self.mode = mode
        self.p = p

        if self.mode == 'cls':
            self.transform = self.single_transform
        elif self.mode == 'seg':
            self.transform = self.join_transform

    def join_transform(self, sample):
        if np.random.random() < self.p:
            image, mask = sample['image'], sample['label']

            # Join Random Filp
            f = [1, 0, -1, 2, 2][np.random.randint(0, 5)]  # [1, 0, -1, 2, 2]
            if f != 2:
                image, mask = filp_array(image, f), filp_array(mask, f)

            # Join Random Roate (Only 0, 90, 180, 270)
            k = np.random.randint(0, 4)  # [0, 1, 2, 3]
            image = np.rot90(image, k, (1, 0))  # clockwise
            mask = np.rot90(mask, k, (1, 0))

            sample['image'], sample['label'] = image.copy(), mask.copy()
        return sample

    def single_transform(self, sample):
        if np.random.random() < self.p:
            image = sample['image']

            # Join Random Filp
            f = [1, 0, -1, 2, 2][np.random.randint(0, 5)]  # [1, 0, -1, 2, 2]
            if f != 2:
                image = filp_array(image, f)

            # Random Roate (Only 0, 90, 180, 270)
            k = np.random.randint(0, 4)  # [0, 1, 2, 3]
            image = np.rot90(image, k, (1, 0))  # clockwise

            sample['image'] = image.copy()
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class ColorAugment(object):
    """ ColorJitter data augmentations for ndarray image sized of (H, W, C).
    support single- or multi- band(s) imagery.

    Args:
        dtype: `RGB` or `other`
    Note:
        For RGB imagery, jitter 'hue', 'sat' and 'val', 'contrast' according to
            `hue_shift_limit`, `sat_shift_limit`, `val_shift_limit`, 'contrast', respectively.

        For other type imagery, jitter brightness and contrast of each band,
            according to `brightness` and `contrast`, respectively.
    """
    def __init__(self,
                 hue=0,
                 sat=0,
                 brightness=0,
                 contrast=0,
                 p=0.5,
                 dtype='RGB'):
        self.p = p

        if dtype == 'RGB':
            self.ColorJitter = ttransform.Compose([ttransform.ColorJitter(
                brightness, contrast, sat, hue)])
            self.transform = self.rgb_transform
        else:
            self.brightness = brightness / 2
            self.contrast = contrast / 2
            self.transform = self.other_transform

    def rgb_transform(self, sample):
        if np.random.random() < self.p:
            image = Image.fromarray(sample['image'], 'RGB')
            image = np.asarray(self.ColorJitter(image))
            sample['image'] = image
        return sample

    def other_transform(self, sample):
        if np.random.random() < self.p:
            image = sample['image']

            if len(image.shape) == 2:
                image = image[:, :, np.newaxis]
                image = randomColorAugment(
                    image, self.brightness, self.contrast)
            elif len(image.shape) == 3:
                band_num = image.shape[2]
                for c in range(0, band_num):
                    image[:, :, c] = randomColorAugment(
                        image[:, :, c], self.brightness, self.contrast)
            else:
                raise TypeError("image and label should be [HW] or [HWC]")

            sample['image'] = image

        return sample

    def __call__(self, sample):
        return self.transform(sample)


class RandomBlur(object):
    """ Randomly blur image sized of [HW] or [HWC],
    support single- or multi- band(s) imagery.

    Args:
        ksize: (int) the kernel size
        type: (str) the type of blur
        p: (float) Probability of diverse noises being applied.
    """
    def __init__(self, ksize=3, ktype='mean', sigma=[.1, 2.], p=0.5):
        self.p = p
        self.ksize = ksize
        self.ktype = ktype
        self.sigma = sigma

        self.blur = {
            'mean': cv2.blur, 'median': cv2.medianBlur, 'gaussian': cv2.GaussianBlur
        }[ktype]
        self.kwargs = {'ksize': (self.ksize, self.ksize)}

    def __call__(self, sample):
        if np.random.random() < self.p:
            # sample['image'] = blur(sample['image'], self.ksize)
            image = sample['image']
            if self.ktype == 'gaussian':  # TODO: too slowly
                sigma = np.random.uniform(self.sigma[0], self.sigma[1])
                self.kwargs.update({'sigmaX': sigma, 'sigmaY': sigma})
            if len(image.shape) == 2 or image.shape[2] < 4:
                image = self.blur(image, **self.kwargs)
            else:
                for c in range(image.shape[2]):
                    band = image[:, :, c]
                    image[:, :, c] = self.blur(band, **self.kwargs)
            sample['image'] = image

        return sample


class RandomNoise(object):
    """ Randomly add a kind of noise on image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        modes: (string list) a set of noise patterns that may be applied to the image,
            but only one at a time.
            - 'gaussian'  Gaussian-distributed additive noise.
            - 'localvar'  Gaussian-distributed additive noise, with specified
                        local variance at each point of `image`.
            - 'poisson'   Poisson-distributed noise generated from the data.
            - 'salt'      Replaces random pixels with 1.
            - 'pepper'    Replaces random pixels with 0 (for unsigned images) or
                        -1 (for signed images).
            - 's&p'       Replaces random pixels with either 1 or `low_val`, where
                        `low_val` is 0 for unsigned images or -1 for signed
                        images.
            - 'speckle'   Multiplicative noise using out = image + n*image, where
                        n is uniform noise with specified mean & variance.
        p: (float) Probability of diverse noises being applied.
    """
    def __init__(self, modes=['gaussian', 's&p'], p=0.5):
        self.p = p
        self.modes = modes

    def __call__(self, sample):
        if np.random.random() < self.p:
            sample['image'] = random_noise(sample['image'], mode=np.random.choice(self.modes))

        return sample


class RandomGrayscale(object):
    """Randomly convert image to grayscale with a probability of p (default 0.1).

    Args:
        p (float): probability that image should be converted to grayscale.
        grayway (str): `mean` or `one`.
            'mean': take mean of each band.
            'one': random choice one band

        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
    """
    def __init__(self, p=0.1, grayway='mean'):
        self.p = p
        self.grayscale = {'mean': self.grayscale_mean,
                          'one': self.grayscale_one}[grayway]

    def grayscale_mean(self, image):
        band_num = image.shape[2]
        gary_img = np.mean(image, axis=2, keepdims=True).astype(np.uint8)
        image = np.repeat(gary_img, band_num, axis=2)
        return image

    def grayscale_one(self, image):
        band_num = image.shape[2]
        gray_band = np.random.randint(0, band_num)
        image = image[:, :, gray_band]
        image = np.repeat(np.expand_dims(image, axis=2), band_num, axis=2)
        return image

    def __call__(self, sample):
        image = sample['image']

        if len(image.shape) == 3:
            if np.random.random() < self.p:
                image = self.grayscale(image)
        sample['image'] = image
        return sample


class ToTensor(object):
    """ Convert `numpy.ndarray` image sized of [H,W] or [H,W,C] in the range [0, 255]
    to a torch.FloatTensor tensor of shape [C, H, W] in the range [0.0, 1.0].

    Args:
        sample
            - if sample is a dict in format of {'image': image}, return dict.
            - if sample is a numpy.ndarray, return ndarray.
    """
    def __call__(self, sample):
        if isinstance(sample, dict):
            image = sample['image']
            if len(image.shape) < 3:
                image = image[:, :, np.newaxis]
            # [H,W,C] array -> [C,H,W] tensor
            image = torch.from_numpy(image.copy().transpose((2, 0, 1)))
            image = image.float().div_(255)
            sample['image'] = image.contiguous()
        elif isinstance(sample, np.ndarray):
            if len(sample.shape) < 3:
                sample = sample[:, :, np.newaxis]
            sample = torch.from_numpy(sample.copy().transpose((2, 0, 1)))
            sample = sample.float().div_(255).contiguous()
        else:
            raise TypeError(
                "Input should be {'image': image array} or image array. Got {}".format(
                    type(sample)))
        return sample


class ToTensor2(object):
    """ Convert image and (may be with) label to tensor.

    Args:
        sample = {'image': image, 'label': label}

    Return:
        {'image': img_tensor, 'label', lbl_tensor}, where img_tensor is a
        torch.FloatTensor of shape [C, H, W] in the range [0.0, 1.0],
        lbl_tensor a torch.LongTensor.
    """
    def __call__(self, sample):
        img = sample['image'].copy()

        if isinstance(img, np.ndarray):
            if len(img.shape) < 3:
                img = img[:, :, np.newaxis]
            # [H,W,C] array -> [C,H,W] tensor
            img = torch.from_numpy(img.copy().transpose((2, 0, 1)))
            img = img.float().div_(255)
        else:
            raise TypeError(
                "Input image should be ndarray, got {}".format(type(img)))
        sample['image'] = img

        if 'label' in sample:
            lbl = sample['label']
            if isinstance(lbl, np.ndarray):
                sample['label'] = torch.from_numpy(lbl).long()
            else:
                sample['label'] = torch.tensor(lbl).long()

        return sample


class Normalizer(object):
    """
    Normalize image which is a Tensor of size (C, H, W), C maybe more than three!

    Args:
        sample (dict): {'image': image, 'label': label},
        mean (sequence): Sequence of means for each channel (R,G,B,NIR, SAR).
        std (sequence): Sequence of standard deviations for each channely.
    """
    def __init__(self, mean, std):
        if mean is None:
            self.mean = [0.5, 0.5, 0.5]
        else:
            self.mean = mean
        if std is None:
            self.std = [0.3125, 0.3125, 0.3125]
        else:
            self.std = std

    def __call__(self, sample):
        if isinstance(sample, dict):
            for t, m, s in zip(sample['image'], self.mean, self.std):
                t.sub_(m).div_(s)
        elif isinstance(sample, np.ndarray):
            for t, m, s in zip(sample, self.mean, self.std):
                # t.sub_(m).div_(s)
                raise NotImplementedError
        elif isinstance(sample, torch.Tensor):
            for t, m, s in zip(sample, self.mean, self.std):
                t.sub_(m).div_(s)
        else:
            raise TypeError(
                "Input should be {'image': image array} or image array. Got {}".format(
                    type(sample)))
        return sample


class UnNormalizer(object):
    """
    UnNormalize image which is a Tensor of size (C, H, W), C maybe more than three!

    Args:
        sample (dict): {'image': image, 'label': label},
    """
    def __init__(self, mean=None, std=None):
        if mean is None:
            self.mean = [0.5, 0.5, 0.5]
        else:
            self.mean = mean
        if std is None:
            self.std = [0.3125, 0.3125, 0.3125]
        else:
            self.std = std

    def __call__(self, sample):
        if isinstance(sample, dict):
            for t, m, s in zip(sample['image'], self.mean, self.std):
                t.mul_(s).add_(m)
        elif isinstance(sample, np.ndarray):
            for t, m, s in zip(sample, self.mean, self.std):
                # t.sub_(m).div_(s)
                raise NotImplementedError
        elif isinstance(sample, torch.Tensor):
            for t, m, s in zip(sample, self.mean, self.std):
                t.mul_(s).add_(m)
        else:
            raise TypeError(
                "Input should be {'image': image array} or image array. Got {}".format(
                    type(sample)))
        return sample


class RotateAndFlip(object):
    """
    Rotate for image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        flip_code:  -2-no_flip, 0-left/right, 1-up/down, -1 left/right & up/down
        rot_code: 0-no_rot, 1-90, 2-180, 3-270
    """
    def __init__(self, rot_code=0, flip_code=-2, mode='cls'):
        self.mode = mode
        self.rot_code = rot_code
        self.flip_code = flip_code

        if self.mode == 'cls':
            self.transform = self.single_transform
        elif self.mode == 'seg':
            self.transform = self.join_transform

    def join_transform(self, sample):
        image, mask = sample['image'], sample['label']

        # Join Random Filp
        if self.flip_code != -2:
            image = filp_array(image, self.flip_code)
            mask = filp_array(mask, self.flip_code)

        # Join Random Roate (Only 0, 90, 180, 270)
        image = np.rot90(image, self.rot_code, (1, 0))  # clockwise
        mask = np.rot90(mask, self.rot_code, (1, 0))

        sample['image'], sample['label'] = image, mask

        return sample

    def single_transform(self, sample):
        image = sample['image']

        if self.flip_code != -2:
            image = filp_array(image, self.flip_code)

        # Random Roate (Only 0, 90, 180, 270)
        image = np.rot90(image, self.rot_code, (1, 0))  # clockwise

        sample['image'] = image
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class Shift(object):
    """
    Shift image sized of [HW] or [HWC] (maybe with mask),
    support single- or multi- band(s) imagery.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        shift_code: (Row_shft, Col_shift)
    """
    def __init__(self, shift_code=(0, 0), mode='cls'):
        self.mode = mode
        self.shift_code = shift_code

        if self.mode == 'cls':
            self.transform = self.single_transform
        elif self.mode == 'seg':
            self.transform = self.join_transform

    def join_transform(self, sample):
        raise NotImplementedError
        return sample

    def single_transform(self, sample):
        image = sample['image']

        H, W = image.shape[:2]
        dim = len(image.shape)

        pad_params = [(0, 0)] * dim
        # Row_shft
        dy = int(H * self.shift_code[0])
        if dy < 0:
            image = image[:H+dy, :]
            pad_params[0] = (0, -dy)
        elif dy > 0:
            image = image[dy:, :]
            pad_params[0] = (dy, 0)

        dx = int(W * self.shift_code[1])
        if dx < 0:
            image = image[:, :W+dx]
            pad_params[1] = (0, -dx)
        elif dx > 0:
            image = image[:, dx:]
            pad_params[1] = (dx, 0)

        sample['image'] = np.pad(image, pad_params, 'constant')
        return sample

    def __call__(self, sample):
        return self.transform(sample)


class Grayscale(object):
    """Convert image to grayscale.

    Args:
        sample (dict): {'image': image, 'label': mask} (both are ndarrays)
        p (float): probability that image should be converted to grayscale.

    Returns:
        ndarray: Grayscale version of the input image with probability p and unchanged
        with probability (1-p).
        - If input image is 1 channel: grayscale version is 1 channel
        - If input image is multi- channel: grayscale version is random single channel
            of input image and return the output image with same shape as input image.

    """
    def __init__(self, band=None):
        self.band = band

    def __call__(self, sample):
        image = sample['image']

        if len(image.shape) == 3:
            band_num = image.shape[2]
            if (self.band is not None) and (self.band < band_num):
                gray_img = image[:, :, self.band]
                image = np.expand_dims(gray_img, axis=2)
            else:
                gary_img = np.mean(image, axis=2, keepdims=True).astype(np.uint8)
            image = np.repeat(gary_img, band_num, axis=2)
        sample['image'] = image
        return sample


def unnormalize(tensor, mean, std, to_array=False, pil=False):
    ''' Input [NCHW] tensor'''
    if len(tensor.shape) == 2:
        tensor = tensor[None, None, :]
    elif len(tensor.shape) == 3:
        tensor = tensor.unsqueeze(dim=0)
    for n in range(tensor.shape[0]):
        for t, m, s in zip(tensor[n, :], mean, std):
            t.mul_(s).add_(m)

    if to_array:
        array = (tensor * 255).permute(0, 2, 3, 1).cpu().numpy().astype(np.uint8)
        if pil:
            return Image(array, 'RGB')
        return array
    return tensor


if __name__ == "__main__":
    # test()
    pass
