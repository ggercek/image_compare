#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `similarity` module."""
import unittest
from image_compare.models import FilePair
from image_compare.exceptions import FileError, ArgumentError
from image_compare.similarity import get_similarity_measurement

class TestSimilarity(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_supported_methods(self):
        for method_name in ["ssim", "nrmse", "dhash", "phash", "whash", "avghash"]:
            method = get_similarity_measurement(method_name)
            assert method is not None

    def test_unsupported_methods(self):
        with self.assertRaises(ArgumentError):
            method = get_similarity_measurement(None)

        with self.assertRaises(ArgumentError):
            method = get_similarity_measurement("")


class TestSSIMSimilarity(unittest.TestCase):
    """Tests for `SSIM` method."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.ssim = get_similarity_measurement("ssim")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_ssim_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        with self.assertRaises(FileError):
            self.ssim(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_ssim_missing_file_second_argument(self):
        pair = FilePair("files/tests/images/0-0-white.png", "no_such_file_exists.png")
        with self.assertRaises(FileError):
            self.ssim(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_ssim_files_with_different_sizes(self):
        pair = FilePair("files/tests/images/1-0-small-white.png", "files/tests/images/1-1-big-white.png")
        with self.assertRaises(ArgumentError):
            self.ssim(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_ssim_similarity_of_same_file_white(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-0-white.png")
        self.ssim(pair)
        assert pair.similarity <= .005, "Same files should return zero"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_of_white_grey(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-2-grey.png")
        self.ssim(pair)
        assert pair.similarity >= 0, "Files are not same, should be a positive value"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_of_white_grey_inverse_order(self):
        pair = FilePair("files/tests/images/0-2-grey.png", "files/tests/images/0-0-white.png")
        self.ssim(pair)
        assert pair.similarity >= 0, "Files are not same, should be a positive value"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_of_white_black(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-1-black.png")
        self.ssim(pair)
        assert pair.similarity >= .995, f"Files are the opposite, should be one {pair.similarity}"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/0-1-black.png", "files/tests/images/0-0-white.png")
        self.ssim(pair)
        assert pair.similarity >= .995, f"Files are the opposite, should be one {pair.similarity}"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_big_files_big_wm_cat(self):
        pair = FilePair("files/tests/images/small/cat.png", "files/tests/images/small/cat-wm-big.png")
        self.ssim(pair)
        assert pair.similarity <= .03
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_ssim_similarity_big_files_small_wm_cat(self):
        pair = FilePair("files/tests/images/small/cat.png", "files/tests/images/small/cat-wm-small.png")
        self.ssim(pair)
        assert pair.similarity <= .01
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False


class TestNRMSESimilarity(unittest.TestCase):
    """Tests for `NRMSE` method."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.nrmse = get_similarity_measurement("nrmse")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_nrmse_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        with self.assertRaises(FileError):
            self.nrmse(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_nrmse_similarity_of_white_black(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-1-black.png")
        self.nrmse(pair)
        assert pair.similarity >= .995, "Files are the opposite, should be one"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_nrmse_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/0-1-black.png", "files/tests/images/0-0-white.png")
        self.nrmse(pair)
        assert pair.similarity >= .995, "Files are the opposite, should be one"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False


class TestDHashSimilarity(unittest.TestCase):
    """Tests for `DHash` method."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.dhash = get_similarity_measurement("dhash")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_dhash_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        with self.assertRaises(FileError):
            self.dhash(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_dhash_similarity_of_same_file_white(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-0-white.png")
        self.dhash(pair)
        assert pair.similarity <= .005, "Same files should return zero"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_dhash_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/small/cat.png", "files/tests/images/small/cat-wm-big.png")
        self.dhash(pair)
#        assert pair.similarity > 0
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False


class TestAvgHashSimilarity(unittest.TestCase):
    """Tests for `AvgHash` method."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.avghash = get_similarity_measurement("avghash")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_avghash_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        with self.assertRaises(FileError):
            self.avghash(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_avghash_similarity_of_same_file_white(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-0-white.png")
        self.avghash(pair)
        assert pair.similarity <= .005, "Same files should return zero"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_avghash_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/small/cat.png", "files/tests/images/small/cat-wm-big.png")
        self.avghash(pair)
#        assert pair.similarity > 0
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False


class TestPHashSimilarity(unittest.TestCase):
    """Tests for `PHash` method."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.phash = get_similarity_measurement("phash")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_phash_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        with self.assertRaises(FileError):
            self.phash(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_phash_similarity_of_same_file_white(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-0-white.png")
        self.phash(pair)
        assert pair.similarity <= .005, "Same files should return zero"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_phash_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/small/cat.png", "files/tests/images/small/cat-wm-big.png")
        self.phash(pair)
        assert pair.similarity > 0
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False


class TestWHashSimilarity(unittest.TestCase):
    """Tests for `WHash` method."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.whash = get_similarity_measurement("avghash")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_whash_missing_file_first_argument(self):
        pair = FilePair("no_such_file_exists.png", "files/tests/images/0-0-white.png")
        with self.assertRaises(FileError):
            self.whash(pair)
        assert pair.skipped is True
        assert pair.similarity == -1.0
        assert pair.elapsed == -1.0

    def test_whash_similarity_of_same_file_white(self):
        pair = FilePair("files/tests/images/0-0-white.png", "files/tests/images/0-0-white.png")
        self.whash(pair)
        assert pair.similarity <= .005, "Same files should return zero"
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False

    def test_whash_similarity_of_white_black_inverse_order(self):
        pair = FilePair("files/tests/images/small/cat.png", "files/tests/images/small/cat-wm-big.png")
        self.whash(pair)
#        assert pair.similarity > 0
        assert pair.elapsed > 0, "Elapsed should be bigger than zero"
        assert pair.skipped is False
