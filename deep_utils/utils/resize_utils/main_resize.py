import numpy as np


def resize(mode, img, dsize, **kwargs):
    if mode == 'normal':
        new_img = cv2_resize(img,
                             dsize=dsize,
                             dst=kwargs.get('dst', None),
                             fx=kwargs.get('fx', None),
                             fy=kwargs.get('fy', None),
                             interpolation=kwargs.get('interpolation', None))
    else:
        raise Exception(f'{mode} is not supported, supported types: normal, ')
    return new_img


def cv2_resize(img, dsize, dst=None, fx=None, fy=None, interpolation=None):
    import cv2
    if len(img.shape) == 3:
        return cv2.resize(img, dsize, dst, fx, fy, interpolation)
    elif len(img.shape) == 4:
        return np.array([cv2.resize(im, dsize, dst, fx, fy, interpolation) for im in img])


def get_img_shape(img):
    if len(img.shape) == 4:
        return img.shape
    elif len(img.shape) == 3:
        return np.expand_dims(img, axis=0).shape
    else:
        raise Exception(f'shape: {img.shape} is not an image')