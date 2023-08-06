# -*- coding:utf-8 -*-
'''
Basic transforms for vision tasks.
Simple package `albumentations`.

Version 1.0  2022-04-04 16:13:09 by QiJi:
'''
import albumentations as T_lib
from albumentations.pytorch.transforms import ToTensorV2


def default_transofroms_for_cls(
    train=True,
    input_size=(224, 224),
    mean=[0.5, 0.5, 0.5],
    std=[0.5, 0.5, 0.5],
    scale=(0.8, 1),
    normalize=True,
    **kwargs
):
    print('default_transofroms_for_cls')
    data_transforms = []

    # * sptial transforms *
    if train:
        data_transforms = [
            T_lib.RandomResizedCrop(*input_size, scale, always_apply=True),
            T_lib.HorizontalFlip(p=0.5),
        ]
    else:
        data_transforms = [
            T_lib.Resize(*input_size, always_apply=True),
        ]

    # * basic data transforms *
    if normalize:
        data_transforms.append(
            T_lib.Normalize(mean, std, always_apply=True))
    data_transforms.append(ToTensorV2())

    return T_lib.Compose(data_transforms)


def normal_transofroms_for_cls(
    train=True,
    input_size=(224, 224),
    mean=[0.5, 0.5, 0.5],
    std=[0.5, 0.5, 0.5],
    scale=(0.8, 1),
    jitter_strength=1.,
    normalize=True,
    **kwargs
):
    print('normal_transofroms_for_cls')
    data_transforms = []
    # * sptial transforms *
    if train:
        data_transforms = [
            T_lib.RandomResizedCrop(*input_size, scale, always_apply=True),
            T_lib.HorizontalFlip(p=0.5),
            T_lib.ColorJitter(
                0.2 * jitter_strength, 0.2 * jitter_strength, 0.2 * jitter_strength,
                0.1 * jitter_strength, p=0.8),
            T_lib.ToGray(p=0.2)
        ]
    else:
        data_transforms = [
            T_lib.Resize(*input_size, always_apply=True),
        ]

    # * basic data transforms *
    if normalize:
        data_transforms.append(
            T_lib.Normalize(mean, std, always_apply=True))
    data_transforms.append(ToTensorV2())

    return T_lib.Compose(data_transforms)


