"""This module contains the wrapper classes for scikit-image library methods"""

import time
from skimage import io, img_as_float
from skimage.measure import compare_ssim as ssim
from skimage.measure import compare_nrmse as nrmse
from skimage.measure import compare_mse as mse

from image_compare.exceptions import FileError, ArgumentError


# TODO: move this to an absctract class
def time_similarity_calculation_and_update_pair(method, timing_method=time.process_time):
    """This decorator will measure the time of the execution
     of decorated function and update the pair parameter pass to that function.
     Process_time excludes time elapsed during sleep, if sleep time is important time.perf_counter() can be used.
     See the documentation;
      * process_time: https://docs.python.org/3/library/time.html#time.process_time
      * perf_counter: https://docs.python.org/3/library/time.html#time.perf_counter
    """
    def timed(*args, **kw):
        ts = timing_method()
        result = method(*args, **kw)
        te = timing_method()
        # Skip the first argument that is object
        args[1].elapsed = te - ts
        return result
    return timed


def check_files_and_open(pair, same_size_enforce=True):
    image1 = None
    image2 = None

    try:
        image1 = io.imread(pair.image1)
    except FileNotFoundError:
        pair.skipped = True
        raise FileError("File Not Found", pair.image1)
    try:
        image2 = io.imread(pair.image2)
    except FileNotFoundError:
        pair.skipped = True
        raise FileError("File Not Found", pair.image2)

    if same_size_enforce and image1.size != image2.size:
        pair.skipped = True
        raise ArgumentError(f"Images should be same size, "
                            "[line:{pair.line_num}]:{pair.image1}[{image1.size}], {pair.image2}[image2.size)]")

    return image1, image2


class StructuralSimilarityIndexMeasure:
    """Compute the mean structural similarity index between two images."""

    @time_similarity_calculation_and_update_pair
    def calculate_similarity(self, pair, coloredImages=True):
        image1, image2 = check_files_and_open(pair)
        img1f = img_as_float(image1)
        img2f = img_as_float(image2)
        similarity = ssim(img1f, img2f, multichannel=True)
        pair.similarity = round(1 - similarity, 3)


class NormalizedRootMeanSquaredErrorMeasure:
    """Compute the normalized root mean-squared error (NRMSE) between two images."""

    @time_similarity_calculation_and_update_pair
    def calculate_similarity(self, pair):
        image1, image2 = check_files_and_open(pair)
        img1f = img_as_float(image1)
        img2f = img_as_float(image2)
        similarity = nrmse(img1f, img2f)
        pair.similarity = round(similarity, 3)


class MeanSquaredErrorMeasure:
    """Compute the mean-squared error between two images."""

    @time_similarity_calculation_and_update_pair
    def calculate_similarity(self, pair):
        image1, image2 = check_files_and_open(pair)
        similarity = mse(image1, image2)
        pair.similarity = round(similarity / float(image1.shape[0] * image1.shape[1]), 3)
