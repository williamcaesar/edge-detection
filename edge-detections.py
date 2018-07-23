#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy
from cv2 import cv2
from image_operations import sumImages as sum_images
from image_operations import show


def add_zero(matrix):
    """Create rows of zeroes and put them on begining or the tail of the array."""
    if len(matrix.shape) == 2:
        matrix = numpy.insert(matrix, 0, 0, axis=1)
        matrix = numpy.insert(matrix, matrix.shape[1], 0, axis=1)
        row01 = numpy.zeros((matrix.shape[1]), numpy.uint8)
        matrix = numpy.insert(matrix, 0, row01, axis=0)
        matrix = numpy.insert(matrix, matrix.shape[0], row01, axis=0)

    if len(matrix.shape) == 3:
        pixel = numpy.zeros((matrix.shape[2]), numpy.uint8)
        matrix = numpy.insert(matrix, 0, pixel, axis=1)
        matrix = numpy.insert(matrix, matrix.shape[1], pixel, axis=1)
        row = numpy.zeros((1, matrix.shape[1], 3), numpy.uint8)
        matrix = numpy.insert(matrix, 0, row, axis=0)
        matrix = numpy.insert(matrix, matrix.shape[0], row, axis=0)

    return matrix


def apply_mask(image, mask, row, column, channel=-1):
    """Apply a mask."""
    if len(image.shape) == 2:
        row01 = int(image[row-1, column-1])*mask[0] + \
            int(image[row-1, column])*mask[1] + \
            int(image[row-1, column+1])*mask[2]

        row02 = int(image[row, column-1])*mask[3] + \
            int(image[row, column])*mask[4] + \
            int(image[row, column+1])*mask[5]

        row03 = int(image[row+1, column-1])*mask[6] + \
            int(image[row+1, column])*mask[6] + \
            int(image[row+1, column+1])*mask[8]
        return row01+row02+row03
    elif channel != -1:
        row01 = int(image[row-1, column-1, channel])*mask[0] + \
            int(image[row-1, column, channel])*mask[1] + \
            int(image[row-1, column+1, channel])*mask[2]

        row02 = int(image[row, column-1, channel])*mask[3] + \
            int(image[row, column, channel])*mask[4] + \
            int(image[row, column+1, channel])*mask[5]

        row03 = int(image[row+1, column-1, channel])*mask[6] + \
            int(image[row+1, column, channel])*mask[7] + \
            int(image[row+1, column+1, channel])*mask[8]

        return row01+row02+row03


def filter(image, mask, div):
    """Apply a filter."""
    if type(mask) != tuple or not(type(div) != float or type(div) != int):
            return
    if len(mask) != 9:
        return
    div = float(div)

    image = add_zero(image)
    print("\nadd zeroes: ", image.shape)

    if len(image.shape) == 2:
        result = numpy.zeros((image.shape[0]-2, image.shape[1]-2), numpy.uint8)
        for row in range(1, image.shape[0]-1):
            for column in range(1, image.shape[1]-1):
                new_pixel = apply_mask(image, mask, row, column)
                result[row-1, column-1] = abs(new_pixel)/div
    else:
        result = numpy.zeros(
            (image.shape[0]-2, image.shape[1]-2, image.shape[2]), numpy.uint8)
        for row in range(1, image.shape[0]-1):
            for column in range(1, image.shape[1]-1):
                for channel in range(0, image.shape[2]):
                    new_pixel = apply_mask(
                        image, mask, row, column, channel)
                    result[row-1, column-1, channel] = abs(new_pixel)/div
    return result


def sobel(image, orientation='vertical or horizontal'):
    """Apply sobel filter."""
    print("Result dimensions ", image.shape)
    vertical_mask = (-1, 0, 1, -2, 0, 2, -1, 0, 1)
    horizontal_mask = (-1, -2, -1, 0, 0, 0, 1, 2, 1)

    if orientation == 'vertical':
        return filter(image, vertical_mask, 4.0)
    elif orientation == 'horizontal':
        return filter(image, horizontal_mask, 4.0)
    else:
        print('orientation must be \'vertical\' or \'horizontal\'')

    vertical_sobel = filter(image, vertical_mask, 4.0)
    horizontal_sobel = filter(image, horizontal_mask, 4.0)
    return sum_images(vertical_sobel, horizontal_sobel)


def prewitt(image, orientation='vertical ou horizontal'):
    """Apply prewitt filter."""
    print("Result dimensions ", image.shape)
    vertical_mask = (-1, 0, 1, -1, 0, 1, -1, 0, 1)
    horizontal_mask = (-1, -1, -1, 0, 0, 0, 1, 1, 1)

    if orientation == 'vertical':
        return filter(image, vertical_mask, 3.0)
    elif orientation == 'horizontal':
        return filter(image, horizontal_mask, 3.0)

    vertical_prewitt = filter(image, vertical_mask, 3.0)
    horizontal_prewitt = filter(image, horizontal_mask, 3.0)
    return sum_images(vertical_prewitt, horizontal_prewitt)


def roberts(image, orientation='vertical ou horizontal'):
    """Apply roberts filter."""
    print("Result dimensions ", image.shape)
    vertical_mask = (0, 0, -1, 0, 1, 0, 0, 0, 0)
    horizontal_mask = (-1, 0, 0, 0, 1, 0, 0, 0, 0)

    if orientation == 'vertical':
        return filter(image, vertical_mask, 3.0)
    elif orientation == 'horizontal':
        return filter(image, horizontal_mask, 3.0)
    else:
        print('orientation must be \'vertical\' or \'horizontal\'')

    roberts_vertical = filter(image, vertical_mask, 3.0)
    horizontal_roberts = filter(image, horizontal_mask, 3.0)
    return sum_images(roberts_vertical, horizontal_roberts)


def isotropic(image, orientation='vertical or horizontal'):
    """Apply isotropic filter."""
    print("Result dimensions ", image.shape)
    vertical_mask = (1, 0, -1, 1.4142135623730951,
                     0, -1.4142135623730951, 1, 0, -1)
    horizontal_mask = (-1, -1.4142135623730951, -1, 0,
                       0, 0, 1, 1.4142135623730951, 1)
    # div = 1
    # div = 1.5
    div = 3.414213562

    if orientation == 'vertical':
        return filter(image, vertical_mask, div)
    elif orientation == 'horizontal':
        return filter(image, horizontal_mask, div)
    else:
        print('orientation must be \'vertical\' or \'horizontal\'')
    vertical_isotropic = filter(image, vertical_mask, div)
    horizontal_isotropic = filter(image, horizontal_mask, div)
    return sum_images(vertical_isotropic, horizontal_isotropic)


if (__name__ == '__main__'):
    image = cv2.imread('images/sapo.png')
    print('original image')
    show(image)
    print('sobel image')
    show(sobel(image))
    print('prewitt image')
    show(prewitt(image))
    print('roberts image')
    show(roberts(image))
    print('isotropic image')
    show(isotropic(image))
