#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `similarity` module."""
import unittest
from image_compare.models import FilePair
from image_compare.exceptions import FileError, ArgumentError
from image_compare.similarity import StructuralSimilarityIndexMeasure, NormalizedRootMeanSquaredErrorMeasure, MeanSquaredErrorMeasure

class TestSSMISimilarity(unittest.TestCase):
    """Tests for `SSIM` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_ssim_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        ssim = StructuralSimilarityIndexMeasure()
        with self.assertRaises(FileError):
            ssim.calculate_similarity(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_ssim_missing_file_second_argument(self):
        pair = FilePair("files/tests/images/0-0-white.png", "no_such_file_exists.png")
        ssim = StructuralSimilarityIndexMeasure()
        with self.assertRaises(FileError):
            ssim.calculate_similarity(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_ssim_files_with_different_sizes(self):
        pair = FilePair("files/tests/images/1-0-small-white.png", "files/tests/images/1-1-big-white.png")
        ssim = StructuralSimilarityIndexMeasure()
        with self.assertRaises(ArgumentError):
            ssim.calculate_similarity(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_ssim_similarity_of_same_file_white(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-0-white.png")
        ssim = StructuralSimilarityIndexMeasure()
        ssim.calculate_similarity(pair)
        assert pair.similarity <= .005, "Same files should return zero"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_of_white_grey(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-2-grey.png")
        ssim = StructuralSimilarityIndexMeasure()
        ssim.calculate_similarity(pair)
        assert pair.similarity >= 0, "Files are not same, should be a positive value"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_of_white_grey_inverse_order(self):
        pair = FilePair("files/tests/images/0-2-grey.png", "files/tests/images/0-0-white.png")
        ssim = StructuralSimilarityIndexMeasure()
        ssim.calculate_similarity(pair)
        assert pair.similarity >= 0, "Files are not same, should be a positive value"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_of_white_black(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-1-black.png")
        ssim = StructuralSimilarityIndexMeasure()
        ssim.calculate_similarity(pair)
        assert pair.similarity >= .995, f"Files are the opposite, should be one {pair.similarity}"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/0-1-black.png", "files/tests/images/0-0-white.png")
        ssim = StructuralSimilarityIndexMeasure()
        ssim.calculate_similarity(pair)
        assert pair.similarity >= .995, f"Files are the opposite, should be one {pair.similarity}"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_big_files_big_wm_cat(self):
        pair = FilePair("files/tests/images/small/cat.png", "files/tests/images/small/cat-wm-big.png")
        ssim = StructuralSimilarityIndexMeasure()
        ssim.calculate_similarity(pair)
        assert pair.similarity <= .03
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_big_files_small_wm_cat(self):
        pair = FilePair("files/tests/images/small/cat.png", "files/tests/images/small/cat-wm-small.png")
        ssim = StructuralSimilarityIndexMeasure()
        ssim.calculate_similarity(pair)
        assert pair.similarity <= .01
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

class TestNRMSESimilarity(unittest.TestCase):
    """Tests for `NRMSE` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_nrmse_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        nrmse = NormalizedRootMeanSquaredErrorMeasure()
        with self.assertRaises(FileError):
            nrmse.calculate_similarity(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_nrmse_similarity_of_white_black(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-1-black.png")
        nrmse = NormalizedRootMeanSquaredErrorMeasure()
        nrmse.calculate_similarity(pair)
        assert pair.similarity >= .995, "Files are the opposite, should be one"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_nrmse_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/0-1-black.png", "files/tests/images/0-0-white.png")
        nrmse = NormalizedRootMeanSquaredErrorMeasure()
        nrmse.calculate_similarity(pair)
        assert pair.similarity >= .995, "Files are the opposite, should be one"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

class TestMSESimilarity(unittest.TestCase):
    """Tests for `MSE` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_mse_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        mse = MeanSquaredErrorMeasure()
        with self.assertRaises(FileError):
            mse.calculate_similarity(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_mse_similarity_of_white_black(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-1-black.png")
        mse = MeanSquaredErrorMeasure()
        mse.calculate_similarity(pair)
#        assert pair.similarity >= .995, "Files are the opposite, should be one"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_mse_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/0-1-black.png", "files/tests/images/0-0-white.png")
        mse = MeanSquaredErrorMeasure()
        mse.calculate_similarity(pair)
#        assert pair.similarity >= .995, "Files are the opposite, should be one"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_mse_similarity_of_same_file_white(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-0-white.png")
        mse = MeanSquaredErrorMeasure()
        mse.calculate_similarity(pair)
        assert pair.similarity <= .005, "Same files should return zero"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False
