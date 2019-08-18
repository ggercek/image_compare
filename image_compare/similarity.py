# -*- coding: utf-8 -*-
"""This module contains the wrapper classes for scikit-image library methods"""

import time
import imagehash
from PIL import Image
from collections import defaultdict
from skimage import io, img_as_float
from skimage.measure import compare_ssim as ssim
from skimage.measure import compare_nrmse as nrmse
from skimage.measure import compare_mse as mse

from image_compare.exceptions import FileError, ArgumentError


MEASUREMENTS = defaultdict(None)


def get_supported_similarity_methods():
    """Returns the supported similarity measurement methods as a list

    :return: supported_methods: list
    """
    return MEASUREMENTS.keys() if MEASUREMENTS is not None else []


def get_similarity_measurement(name):
    """ Returns similarity measurement method
    :param name: name of the method ["ssim", "nrmse", "mse"]
    :return: similarity method if the name is valid
    :raises:
        ArgumentError: if name is a not a valid implemented method
    """
    method = MEASUREMENTS.get(name)
    if method is None:
        raise ArgumentError(f"{name} is a not a supported similarity method")

    return method


def register_distance(name=""):
    """Registers the similarity method with given name to MEASUREMENTS dictionary

    :param name: name of the method e.g ssim, nrmse, mse, etc.
    :return: decorated method
    """
    def decorator_register(func):
        """Decorator to register similarity measurments"""
        MEASUREMENTS[name] = func

    return decorator_register


class TimeSimilarityCalculation:
    """Measures the time of the execution of decorated function and
    update the pair parameter pass to that function.

    :param method: similarity method to decorate
    :param timing_method: timing method to use, default value is time.process_time
    Process_time excludes time elapsed during sleep, if sleep time is important time.perf_counter() can be used.
     See the documentation;
      * process_time: https://docs.python.org/3/library/time.html#time.process_time
      * perf_counter: https://docs.python.org/3/library/time.html#time.perf_counter
    :return: the result of decorated function
    """

    def __init__(self, timing_method=time.process_time):
        self.timing_method = timing_method

    def __call__(self, method):
        def timed(*args, **kw):
            ts = self.timing_method()
            result = method(*args, **kw)
            te = self.timing_method()
            # Update pair's elapsed time
            args[0].elapsed = te - ts
            return result
        return timed


def __check_files_and_open_with_pil(pair, same_size_enforce=True):
    return __check_files_and_open(pair, same_size_enforce=same_size_enforce, image_read_func=Image.open)


def __check_files_and_open(pair, same_size_enforce=True, image_read_func=io.imread):
    """Private function that enforces common checks and returns the file handlers

    :param pair: `FilePair` object
    :param same_size_enforce: enables dimension check of image pairs
    :return:
        image1, image2 : ndarray, ndarray
        loaded images
    :raises:
        FileError: if an image is missing
        ArgumentError: if same_size_enforce=True and images have different dimensions
    """

    image1 = None
    image2 = None

    try:
        image1 = image_read_func(pair.image1)
    except FileNotFoundError:
        pair.skipped = True
        raise FileError("File Not Found", pair.image1)
    try:
        image2 = image_read_func(pair.image2)
    except FileNotFoundError:
        pair.skipped = True
        raise FileError("File Not Found", pair.image2)

    if same_size_enforce and image1.size != image2.size:
        pair.skipped = True
        raise ArgumentError(f"Images should be same size, "
                            f"[line:{pair.line_num}]:{pair.image1}[{image1.size}], {pair.image2}[image2.size)]")

    return image1, image2


@register_distance(name="ssim")
@TimeSimilarityCalculation()
def calculate_ssim_similarity(pair):
    """Compute the mean structural similarity index between two images.

    :param pair: image pair to compare
    :return:
    """
    image1, image2 = __check_files_and_open(pair)
    img1f = img_as_float(image1)
    img2f = img_as_float(image2)
    similarity = ssim(img1f, img2f, multichannel=True)
    pair.similarity = round(1 - similarity, 3)


@register_distance(name="nrmse")
@TimeSimilarityCalculation()
def calculate_nrmse_similarity(pair):
    """Compute the normalized root mean-squared error (NRMSE) between two images.

    :param pair: image pair to compare
    :return:
    """
    image1, image2 = __check_files_and_open(pair)
    img1f = img_as_float(image1)
    img2f = img_as_float(image2)
    similarity = nrmse(img1f, img2f)
    pair.similarity = round(similarity, 3)


@register_distance(name="mse")
@TimeSimilarityCalculation()
def calculate_mse_similarity(pair):
    """Compute the mean-squared error between two images.

    :param pair: image pair to compare
    :return:
    """
    image1, image2 = __check_files_and_open(pair)
    similarity = mse(image1, image2)
    pair.similarity = round(similarity / float(image1.shape[0] * image1.shape[1]), 3)


@TimeSimilarityCalculation()
def __calculate_imagehash_based_similarity(pair, hash_func, hash_size=16):
    """Compute given hash_func over pair object's images and update pair object's similarity"""
    image1_handle = None
    image2_handle = None
    try:
        image1_handle, image2_handle = __check_files_and_open_with_pil(pair)
        image1 = hash_func(image1_handle, hash_size=hash_size)
        image2 = hash_func(image2_handle, hash_size=hash_size)
        pair.similarity = float(image1 - image2) / hash_size
    finally:
        # close the image files
        if image1_handle:
            image1_handle.close()
        if image2_handle:
            image2_handle.close()


@register_distance(name="dhash")
def calculate_dhash_similarity(pair, hash_size=16):
    """Compute Difference Hash"""
    __calculate_imagehash_based_similarity(pair, imagehash.dhash, hash_size=hash_size)


@register_distance(name="avghash")
def calculate_avghash_similarity(pair, hash_size=16):
    """Compute Average Hash"""
    __calculate_imagehash_based_similarity(pair, imagehash.average_hash, hash_size=hash_size)


@register_distance(name="phash")
def calculate_phash_similarity(pair, hash_size=16):
    """Compute Perception Hash"""
    __calculate_imagehash_based_similarity(pair, imagehash.phash, hash_size=hash_size)


@register_distance(name="whash")
def calculate_whash_similarity(pair, hash_size=16):
    """Compute Wavelet Hash"""
    __calculate_imagehash_based_similarity(pair, imagehash.whash, hash_size=hash_size)
