'''
Tools collection of Data(np.ndarray) processing.

Version 1.0  2018-04-03 15:44:13 by QiJi
Version 1.5  2018-04-07 22:34:53 by QiJi
Version 2.0  2018-04-11 09:43:47 by QiJi
    Add MyData class, rename this model names and some functions name
Version 3.0  2018-10-25 16:59:23 by QiJi
'''
import os
import sys
import random
import math
from matplotlib import pyplot as plt
import cv2
import numpy as np
from tqdm import tqdm
from .fileop import filelist, mkdir_nonexist


def get_data_dir(ds, data_dir):
    if type(data_dir) == str:
        return data_dir
    elif type(data_dir) == dict:
        return data_dir[ds]


# **********************************************
# *************** Dataset statics **************
# **********************************************
def print_static_dict_in_md(static_dict, log_file=None, verbose=True, dict_level='1', nshort=1e8):
    """ Print category statistical info. (dict) in markdown.

    Args:
        dict_level:  Number of levels in the category statistical dict
    """
    assert dict_level in ['1', '2']
    if nshort == 1:
        nshort = 1e8

    if dict_level == '1':
        statis_str = '| Class | Num |\r\n|-|-|\r\n'
        total_num = 0
        for cls, cls_num in sorted(static_dict.items()):
            if cls == 'total':
                continue
            cls_num = min(cls_num, nshort)  #

            total_num += cls_num
            statis_str += '| {} | {} |\r\n'.format(cls, cls_num)
            # print(len(names))
        statis_str += '| Total | {} |'.format(total_num)

    elif dict_level == '2':
        statis_str = '| Class_L1 | Class_L2 | Num |\r\n|-|-|-|\r\n'
        total_num = 0
        for cls_L1, scene_statis_L1 in sorted(static_dict.items()):
            statis_str += '| {} | total |  {} |\r\n'.format(cls_L1, scene_statis_L1['total'])
            # total_num += static_dict[cls_L1]['total']
            for cls_L2, cls_L2_num in sorted(scene_statis_L1.items()):
                if cls_L2 == 'total':
                    continue
                cls_L2_num = min(cls_L2_num, nshort)

                total_num += cls_L2_num
                statis_str += '| - | {} |  {} |\r\n'.format(cls_L2, cls_L2_num)

        statis_str += '| ALL Total | - | {} |'.format(total_num)

    if verbose:
        print(statis_str)
    if log_file:
        with open(log_file, 'w') as f:
            f.write(statis_str)

    return statis_str


def compute_class_weights(labels_dir, label_values):
    '''
    Arguments:
        labels_dir(list): Directory where the image segmentation labels are
        num_classes(int): the number of classes of pixels in all images

    Returns:
        class_weights(list): a list of class weights where each index represents
            each class label and the element is the class weight for that label.

    '''
    image_files = filelist(labels_dir, ifPath=True, extension='.png')
    num_classes = len(label_values)
    class_pixels = np.zeros(num_classes)
    total_pixels = 0.0

    for n in range(len(image_files)):
        image = cv2.imread(image_files[n], -1)
        for index, colour in enumerate(label_values):
            class_map = np.all(np.equal(image, colour), axis=-1)
            class_map = class_map.astype(np.float32)
            class_pixels[index] += np.sum(class_map)

        print("\rProcessing image: " + str(n) + " / " + str(len(image_files)), end="")
        sys.stdout.flush()

    total_pixels = float(np.sum(class_pixels))
    index_to_delete = np.argwhere(class_pixels == 0.0)
    class_pixels = np.delete(class_pixels, index_to_delete)
    class_weights = total_pixels / class_pixels
    class_weights = class_weights / np.sum(class_weights)

    return class_weights


def get_dataset_class_names(in_dir, verbose=False):
    folders = os.listdir(in_dir)
    class_names = []
    for fld in folders:
        if os.path.isdir(os.path.join(in_dir, fld)):
            class_names.append(fld)
    class_names = sorted(class_names)
    if verbose:
        print(class_names)
    return class_names


def static_cls_sample_num(in_dir, class_names=None):
    if class_names is None:
        class_names = get_dataset_class_names(in_dir)

    scene_statics = {'total': 0}
    for cls in sorted(class_names):
        cls_dir = os.path.join(in_dir, cls)
        names = os.listdir(cls_dir)
        scene_statics[cls] = len(names)
        scene_statics['total'] += len(names)

    print_static_dict_in_md(scene_statics, verbose=True)

# **************************************************
# *********** Tools for visualization **************
# **************************************************
def dataset_classwise_thumbnail(in_dir, vis_dir=None, max_num=100, class_names=None, dpi=2):
    """ Generate sample thumbnail of dataset """
    if vis_dir is None:
        vis_dir = in_dir + '_classwise_thumbnail'
    mkdir_nonexist(vis_dir)

    if class_names is None:
        class_names = get_dataset_class_names(in_dir)

    # print('| Class | Num |\r\n|-|-|')
    for cls in tqdm(sorted(class_names)):
        cls_dir = os.path.join(in_dir, cls)
        names = os.listdir(cls_dir)
        cls_num = len(names)
        use_num = min(cls_num, max_num)
        if use_num < 1:
            continue

        random.shuffle(names)
        samples = names[:use_num]
        # print('| {} | {} |'.format(cls, len(names)))

        rc = max(2, math.ceil(use_num ** 0.5))
        fig, axs = plt.subplots(nrows=rc, ncols=rc, figsize=(rc*dpi, rc*dpi))
        plt.setp(axs.flat, xticks=[], yticks=[])
        fig.suptitle(cls, fontsize=10*dpi)

        for i, name in enumerate(samples):
            img_pth = os.path.join(cls_dir, name)
            img = cv2.imread(img_pth, 1)[:, :, ::-1]
            axs[i // rc, i % rc].imshow(img)

        fig.tight_layout()
        plt.subplots_adjust(top=0.95)
        # plt.show()
        fig.savefig('%s/%s.jpg' % (vis_dir, cls))
        plt.close(fig)

    print('Finish!\n')


def dataset_whole_thumbnail(in_dir, vis_pth=None, num_per_class=2, class_names=None, dpi=2):
    if vis_pth is None:
        vis_pth = in_dir + '_whole_thumbnail'

    if class_names is None:
        class_names = get_dataset_class_names(in_dir)

    num_classes = len(class_names)
    fig, axs = plt.subplots(nrows=num_classes, ncols=num_per_class,
                            figsize=(dpi*num_per_class, dpi*num_classes))
    plt.setp(axs.flat, xticks=[], yticks=[])

    if len(class_names) > 1:
        # for k, cls in enumerate(tqdm(sorted(class_names))):
        for k, cls in enumerate(tqdm(class_names)):
            cls_dir = os.path.join(in_dir, cls)
            names = os.listdir(cls_dir)
            use_num = min(len(names), num_per_class)
            if use_num < 1:
                continue

            random.shuffle(names)
            samples = names[:use_num]

            for i, name in enumerate(samples):
                img_pth = os.path.join(cls_dir, name)
                img = cv2.imread(img_pth, 1)[:, :, ::-1]
                # axs[k, i].set_axis_off()
                # axs[k, i].imshow(cv2.resize(img, (600, 600)))
                axs[k, i].imshow(img)
                # if i == 0:
                #     axs[k, i].set_title(cls, fontsize=2)
        for ax, name in zip(axs[:, 0], class_names):
            ax.set_ylabel(name, size=8*dpi)
    elif len(class_names) == 1:
        cls = class_names[0]
        cls_dir = os.path.join(in_dir, cls)
        names = os.listdir(cls_dir)
        use_num = min(len(names), num_per_class)
        if use_num < 1:
            return

        random.shuffle(names)
        samples = names[:use_num]

        for i, name in enumerate(samples):
            img_pth = os.path.join(cls_dir, name)
            img = cv2.imread(img_pth, 1)[:, :, ::-1]
            axs[i].imshow(img)
        axs[0].set_ylabel(cls, size=8*dpi)
    else:
        return

    # plt.show()
    plt.tight_layout()
    fig.subplots_adjust(left=0.03)
    fig.savefig('%s.jpg' % (vis_pth))
    # plt.close(fig)

    print('Finish!\n')


# **********************************************
# *********** Data Post-treatment **************
# **********************************************
def bwmorph(image, kernel_1=None, kernel_2=None):
    '''
    Do BW morphologic pocessing in label.

    Args:
        image: Tnput image, better be [HW].(also support [HW1] and [HWC])
        kernel_1: The kernel for closses

    Returns:
        image: [HW] label

    Notice: If input label is a multiply channel img, will only keep
        its first channel, then do morphologic pocessing.
    '''
    kernel_0 = np.array([[0, 0, 1, 0, 0],
                         [0, 1, 1, 1, 0],
                         [1, 1, 1, 1, 1],
                         [0, 1, 1, 1, 0],
                         [0, 0, 1, 0, 0]],
                        dtype=np.uint8)
    if kernel_1 is None:
        kernel_1 = kernel_0
    if kernel_2 is None:
        kernel_2 = kernel_0

    if len(image.shape) > 2:
        if image.shape[2] == 3:
            image = image[:, :, 0]
        elif image.shape[2] == 1:
            image = image[:, :, 0]
        else:
            ValueError("What a fucking image U choose?")

    # 闭运算-用[5x5](默认)kernel连接细小断裂
    image = cv2.erode(cv2.dilate(image, kernel_1), kernel_1)

    # 开运算-用[5x5]kernel去除细微噪点
    # kernel = np.ones([5, 5], dtype=np.uint8)
    image = cv2.dilate(cv2.erode(image, kernel_2), kernel_2)

    return image


def vote_combine(label, crop_params, crop_info, mode, scale=False):
    '''
    Combine small scale predicted label into a big one,
    for 1.classification or 2.semantic segmantation.
    Args:
        label: One_hot label(may be tensor). 1.[NC]; 2.[NHWC]
        crop_params: [sub_h, sub_w, crop_stride]
        crop_info: [rows, cols]
            rows: Num of images in the row direction.
            cols: Num of images in the col direction.
        mode: 1-classification, 2-semantic segmantation.
        scale: If do adaptive normalize.
    Returns:
        out_label: [HWC] one hot array, uint8.
    '''
    rows, cols = crop_info
    h, w, stride = crop_params
    label = np.array(label)  # Tensor -> Array
    if mode == 1:
        # 1. For classification
        if len(label.shape) == 3:  # list转array后会多出一维
            label = np.squeeze()
    elif mode == 2:
        # 2. For semantic segmantation
        if len(label.shape) == 5:  # in case of label is [1NHWC]
            label = label[0]
    else:
        return ValueError('Incorrect mode!')
    out_h, out_w = (rows-1)*stride+h, (cols-1)*stride+w
    out_label = np.zeros([out_h, out_w, label.shape[-1]], dtype=label.dtype)  # [HWC]

    y = 0  # y=h=row
    for i in range(rows):
        x = 0  # x=w=col
        for j in range(cols):
            out_label[y:y+h, x:x+w] += label[i*cols+j]  # 此处融合用加法
            x += stride
        y += stride

    # 自适应归一化
    if scale:
        m = np.max(out_label, axis=-1, keepdims=True).repeat(2, -1)
        n = np.min(out_label, axis=-1, keepdims=True).repeat(2, -1)
        out_label = out_label / (m - n)
    return out_label  # np.uint8(out_label)


def modefilter(label):
    '''找到label matrix中所有的无类别值(0), 用8连通区的众数给其赋值. '''
    newlabel = label.copy()
    indlist = np.argwhere(label == 0)
    label = np.pad(label, ((1, 1), (1, 1)), mode='reflect')
    for [r, c] in indlist:  # ind - [r, c]
        try:
            connected = label[r:r+2, c:c+2]
            mode = np.argmax(np.bincount(connected))
        except Exception:
            mode = 0
        newlabel[r, c] = mode
    return newlabel


def modify_label(label, class_set, fixed_value=None):
    """ 将`label`中不正常（没有被`class_set`所包含的）的值设置为`fixed_value`.
    label is an HW ndarray.
    Args:
        class_set: a dict of categories or list of class num.
    """
    if type(class_set) == dict:
        class_set = [key for (_, key) in class_set.items()]
    if type(class_set) != list:
        ValueError('class_set should be a dict of categories or list of class num')
    if fixed_value is None:
        fixed_value = class_set[-1]

    if 255 not in class_set:
        label[label == 255] = fixed_value
    for ii in range(0, np.max(label)+1):
        # if np.sum(label == ii):
        #     print('err value: %d' % ii)
        if ii not in class_set:
            label[label == ii] = fixed_value
    return label


def changelabel(label, mapping):
    ''' Map the categories using input mapping,
    where mapping is dict{orignal_category1: target_category1, ...}
    Note: Input label is [HW]
    '''
    # label_org = label
    label_new = label.copy()

    for (k, v) in mapping.items():
        label_new[label == k] = v
    return label_new


# **********************************************
# ********* Dataset initializaion **************
# **********************************************
def classifydataset_init(root, class_dict=None, ratio=[0.5, 0.3, 0.2], full_train=False, mode=0):
    '''
    分类数据初始化, 即获得训练(测试)集的所有文件路径及其标签
    Args:
        root (string): The dir of the train(test) dataset folder.

        class_dict (dict): {class_name1: ind1, class_name2: ind2, ...}

        ratio - [train, val, test] or [train, val]
            Note: 在2、3种模式下, ratio[0]默认为0,
                若为1则表示train_set包含train/val/test所有数据

        mode - 文件的组织结构不同
            1: 不同类别分文件夹放置
            2: 预测划分了train/val/test
            3. CSU_RSISC sample-level (cls)

        full_train - wether return all the images for train
    '''
    init_dataset = {k: {} for k in ['train', 'val', 'test']}

    def _find_classes(data_dir: str):
        classes = [fld.name for fld in os.scandir(data_dir) if fld.is_dir()]
        classes.sort()
        class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
        return class_to_idx

    if mode == 1:
        if class_dict is None:
            class_dict = _find_classes(root)
        # loop floders
        for cls in class_dict.keys():
            lbl = class_dict[cls]
            cls_dir = root + '/' + cls
            if not os.path.exists(cls_dir):
                print(f'Missing samples belonging to {cls}')
                samples = []
                train_num, val_num = 0, 0
            else:
                img_names = sorted(os.listdir(cls_dir))
                samples = [(cls_dir+'/'+x, lbl) for x in img_names]
                n = len(img_names)
                train_num, val_num = round(n * ratio[0]), round(n * ratio[1])
            if full_train:
                init_dataset['train'].update({cls: samples[:]})
            else:
                init_dataset['train'].update({cls: samples[: train_num]})
            init_dataset['val'].update({cls: samples[train_num: train_num + val_num]})
            init_dataset['test'].update({cls: samples[train_num + val_num:]})

    elif mode == 2:
        if class_dict is None:
            for split in ['train', 'val', 'test']:
                data_dir = root + '/' + split
                if os.path.exists(data_dir):
                    class_dict = _find_classes(data_dir)
                    break
        for split in ['train', 'val', 'test']:
            data_dir = root + '/' + split
            if os.path.exists(data_dir):
                for cls in class_dict.keys():
                    lbl = class_dict[cls]
                    img_names = sorted(os.listdir(data_dir + '/' + cls))
                    samples = [(data_dir+'/'+cls+'/'+x, lbl) for x in img_names]
                    init_dataset[split].update({cls: samples})
                    if full_train and split != 'train':
                        if len(samples) == 0:
                            continue
                        init_dataset['train'][cls].extend(samples)
            else:
                print('No %sing set found at: %s.' % (split, data_dir))

    elif mode == 3:
        # root += '/samples'
        for split in ['train', 'val']:
            init_dataset[split] = []
            img_dir = root + '/{}'.format(split)
            lbl_dir = root + '/{}_labels_patch_level'.format(split)
            if os.path.exists(img_dir) and os.path.exists(lbl_dir):
                for name in sorted(os.listdir(img_dir)):
                    sample_img_pth = img_dir + '/' + name
                    sample_lbl = cv2.imread(lbl_dir + '/' + name, 0)
                    init_dataset[split].append((sample_img_pth, sample_lbl))
                    if full_train and split != 'train':
                        init_dataset['train'].append((sample_img_pth, sample_lbl))
            else:
                print('No %sing set found at: %s.' % (split, img_dir))

    init_dataset['class_dict'] = class_dict
    return init_dataset


def segdataset_init(root, dtype='RGB', full_train=False, mode=0, seed=0):
    '''
    Initilize the segmentation dataset dict:
        {'train': {'image': {'RGB': [img_pths], 'SAR': [img_pths], ...},
                   'label': [lbl_pths]},
         'val': {'image': {'RGB': [img_pths], 'SAR': [img_pths]},
                 'label': [lbl_pths]},
        }
    Args:
        root - The dir of the train(test) dataset folder.
        dtype - The type of data, ['RGB', 'SAR']
        mode - 文件的组织结构不同
            0: 预测划分了train/val/test but only RGB data
            1: 预测划分了train/val/test and have multi-datatype
        full_train - wether return all the images for train
    '''
    init_dataset = {k: {'image': {}, 'label': []} for k in ['train', 'val', 'test']}
    lbl_dir_suffix = ''
    for suffix in ['_lbl', '_label', '_labels']:
        for sp in ['train', 'val', 'test']:
            test_pth = root + '/' + sp + suffix
            if os.path.exists(test_pth):
                lbl_dir_suffix = suffix
                break

    if mode == 0:  # only RGB data
        for sp in ['train', 'val', 'test']:
            lbl_dir = root + '/' + sp + lbl_dir_suffix
            if os.path.exists(lbl_dir):
                lbl_pths = [lbl_dir+'/'+name for name in sorted(os.listdir(lbl_dir))]
                init_dataset[sp]['label'] = lbl_pths
                if full_train and sp != 'train':
                    init_dataset['train']['label'] += lbl_pths
            else:
                print('No %sing set label found at: %s.' % (sp, lbl_dir))
            img_dir = root + '/' + sp
            if os.path.exists(img_dir):
                img_pths = [img_dir+'/'+name for name in sorted(os.listdir(img_dir))]
                init_dataset[sp]['image']['RGB'] = img_pths
                if full_train and sp != 'train':
                    init_dataset['train']['image']['RGB'] += img_pths
            else:
                print('No %sing set image found at: %s.' % (sp, img_dir))

    elif mode == 1:
        for sp in ['train', 'val', 'test']:
            lbl_dir = root + '/' + sp + lbl_dir_suffix
            if os.path.exists(lbl_dir):
                lbl_pths = [lbl_dir+'/'+name for name in sorted(os.listdir(lbl_dir))]
                init_dataset[sp]['label'] = lbl_pths
                if full_train and sp != 'train':
                    init_dataset['train']['label'] += lbl_pths
            else:
                print('No %sing set label found at: %s.' % (sp, lbl_dir))
            for dt in dtype:
                img_dir = root + '/%s_%s' % (sp, dt)
                if os.path.exists(img_dir):
                    img_pths = [img_dir+'/'+name for name in sorted(os.listdir(img_dir))]
                    init_dataset[sp]['image'][dt] = img_pths
                    if full_train and sp != 'train':
                        init_dataset['train']['image'][dt] += img_pths
                else:
                    print('No %sing set image type of %s found at: %s.' % (sp, dt, img_dir))
    return init_dataset


# **********************************************
# ************ Main functions ******************
# **********************************************
def data_statistics(ds_root, band_num=3, ext='.jpg'):
    ''' Count (pixel-level) mean and variance of dataset. '''

    mean = np.zeros(band_num)  # BGR
    std = np.zeros(band_num)  # BGR

    total_image = 0
    # Statisify mean and std
    for root, dirs, files in tqdm(os.walk(ds_root)):
        for name in files:
            if not name.endswith(ext):
                continue
            path = os.path.join(root, name)
            img = cv2.imread(path, cv2.IMREAD_COLOR)  # BGR
            img = np.float64(img)
            for c in img.shape[-1]:
                mean[c] += np.mean(img[:, :, c])
                std[c] += np.std(img[:, :, c])
            total_image += 1

    mean /= total_image
    std /= total_image
    print('mean=', mean)
    print('std=', std)
    print('Careful: BGR!')
    return mean, std


def spilt_dataset(in_floders, out_floders, rate=0.025, max_num=None):
    '''Spilt images(maybe with labels)
    Args:
        in_floders - list of input floders
        out_floders - list of output floders
            for example:
                in_floders = [
                    'dataset_dir/train',
                    'dataset_dir/train_labels'
                ]
                out_floders = [
                    'dataset_dir/val',
                    'dataset_dir/val_labels'
                ]
    '''
    from shutil import move
    # from sklearn.model_selection import train_test_split

    name_list = []
    for d in in_floders:
        names = filelist(d)
        name_list.append(names)
    file_num = len(name_list[0])  # 文件总数
    max_num = file_num if max_num is None else max_num

    # 按比例抽取
    index = np.random.permutation(file_num)
    index = index[:int(file_num*rate)]

    for d, names in zip(range(len(in_floders)), name_list):
        print(in_floders[d])
        cnt = 0
        for i in index:
            # 针对文件的操作
            # os.remove(d+'/'+names[i])
            move(in_floders[d]+'/'+names[i], out_floders[d]+'/'+names[i])
            cnt += 1
            if cnt >= max_num:
                break  # if set max_num, prioritize the max_num

    print('Finished!')


def MorphologicPostTreate(input_dir, output_dir):
    '''
    形态学后处理
    '''
    image_names = filelist(input_dir)
    kernel = np.ones([7, 7], dtype=np.uint8)
    kernel[0, 0], kernel[-1, -1], kernel[0, -1], kernel[-1, 0] = 0, 0, 0, 0
    # print(kernel)

    for i in tqdm(range(len(image_names))):
        img = cv2.imread(input_dir + "/" + image_names[i], -1)
        img = bwmorph(img, kernel_1=kernel)  # 输出[HW]label
        img = np.repeat(np.expand_dims(img, axis=2), 3, axis=2)
        cv2.imwrite(output_dir + "/" + image_names[i], img)


def main():
    pass


if __name__ == '__main__':
    # main()
    data_statistics()
    # spilt_dataset(max_num=1000)
    pass
