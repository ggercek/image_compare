=============
Image Compare
=============


.. image:: https://img.shields.io/pypi/v/image_compare.svg
        :target: https://pypi.python.org/pypi/image_compare

.. image:: https://img.shields.io/travis/ggercek/image_compare.svg
        :target: https://travis-ci.org/ggercek/image_compare

.. image:: https://readthedocs.org/projects/image-compare/badge/?version=latest
        :target: https://image-compare.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ggercek/image_compare/shield.svg
        :target: https://pyup.io/repos/github/ggercek/image_compare/
        :alt: Updates

.. image:: https://coveralls.io/repos/github/ggercek/image_compare/badge.svg?branch=master
        :target: https://coveralls.io/github/ggercek/image_compare?branch=master


CLI tool to compare image similarities.


* Free software: GNU General Public License v3
* Documentation: https://image-compare.readthedocs.io.

.. contents::


How to use
----------
.. code-block::

    Usage: image_compare [OPTIONS] INPUT_FILE OUTPUT_FILE

      A tool to compare given image pairs

    Options:
      --overwrite-output              Overwrite the output if already exists
      --quiet                         Suppress console output
      --distance [ssim|nrmse|mse|dhash|avghash|phash|whash]
                                      Similarity method to compare image pairs
      --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                      Log level to control the output volume
      --help                          Show this message and exit.


    image_compare --distance=ssim --overwrite-output files/product-cat-photos.csv files/product-cat-photos.csv

Features
--------

* Currently supports only CSV input output formats

* Supports multiple comparision method, namely;
    * SSIM:
    * MSE:
    * NRMSE:
    * DHash:
    * AHash:
    * PHash:
    * WHash:


**Sample Files**

.. csv-table:: Sample Input File
   :header: "image1", "image2"
   :widths: 20, 20

   "files/images/cat.png","files/images/cat-box.png"
   "files/images/cat.png","files/images/cat-hue.png"
   "files/images/cat.png","files/images/cat-sampler.png"
   "files/images/cat.png","files/images/cat-wm-big.png"
   "files/images/cat.png","files/images/cat-wm-small.png"

.. csv-table:: Sample Output File
   :header: "image1", "image2", "similarity", "elapsed"
   :widths: 20, 20, 20, 20

   "files/images/cat.png","files/images/cat-box.png",0.016,1.421875
   "files/images/cat.png","files/images/cat-hue.png",0.157,1.390625
   "files/images/cat.png","files/images/cat-sampler.png",0.012,1.40625
   "files/images/cat.png","files/images/cat-wm-big.png",0.014,1.375
   "files/images/cat.png","files/images/cat-wm-small.png",0.005,1.390625

* TODO

Technologies
------------

Following packages used for development and testing

**Development**

* Click==6.0
* scikit-image==0.15.0
* scipy==1.3.1
* imagehash==0.4

**Testing & Building**

* pip==19.2.2
* bump2version==0.5.10
* wheel==0.33.4
* watchdog==0.9.0
* flake8==3.7.8
* tox==3.13.2
* coverage==4.5.4
* Sphinx==2.1.2
* twine==1.13.0
* bandit==1.6.2

Development
-----------

Implementation Details
^^^^^^^^^^^^^^^^^^^^^^

**Modules**

Here is brief description of each module and their components. Also, you can find more info at `Module Index`_

* cli
    contains Command Line Interface(CLI) definition and help text.
    This module parses user's input and creates a `models.Config` object to pass it
    to `image_compare.main(config)` method
    This module contains the entry point of the project.
* exception
    Contains following custom exception classes, for error handling.
    * ICError(Exception): Base exception class
    * FileError(ICError): Represents file related errors
    * ArgumentError(ICError): Represents argument related logic errors
* file_handlers
    Contains the classes for parsing and writing files as well as
    a factory class to object creation based on the input/output file extension.
    This module currently supports only CSV files
    * FileHandlerFactory:
    * CSVInputHandler: Deals with the CSV file parsing and creating FilePair objects
    * CSVOutputHandler: Writes given FilePair objects in to a CSV file.
* image_compare
    This module deals with logging, exception handling and program flow.
* models
    Contains `FilePair` and `Config` data objects.
* similarity
    Contains the similarity calculation methods as well as the timing and registration functionality.
    Please see te `Adding a new similarity measurment` section for implementation details
    Supported methods are : SSIM, MSE, NRMSE, DHash, AHash, WHash, PHash.
    Please see `Method` Section for details.
* util
    Contains utility functions

.. _`Module Index`: https://image-compare.readthedocs.io/en/latest/py-modindex.html

Adding a commandline argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming you want to add a new commandline argument, namely `log-filename`.

1) Update your CLI definition in `image_compare.cli` module. Decorate `image_compare.cli.main()`

    @click.option("--log-filename", default="image_compare.log",help="Log file path")

2) You must add new `log_filename` argument to main() method, updated main method signature should look like this

    def main(input_file, output_file, overwrite_output, quiet, distance, log_level, log_filename):

3) Pass the new argument to Config object

        config = Config(input_file, output_file, overwrite_output, quiet, distance, log_level, log_filename)

4) Update the image_compare.models.Config class and update test for initial values

5) Now you can use `config.log_filename` in `image_compare.main()` method

Final version of `image_compare.cli.main` method

.. code-block:: python
    :linenos:
    :emphasize-lines: 12,13,16

    @click.command()
    @click.argument("input_file")
    @click.argument("output_file")
    @click.option("--overwrite-output", is_flag=True, default=False,
                  help="Overwrite the output if already exists")
    @click.option("--quiet", is_flag=True, default=False,
                  help="Suppress console output")
    @click.option("--distance", type=click.Choice(get_supported_similarity_methods()), default="ssim",
                  help="Similarity method to compare image pairs")
    @click.option("--log-level", type=click.Choice(image_compare.log_levels.keys()), default="INFO",
                  help="Log level to control the output volume")
    @click.option("--log-filename", default="image_compare.log",
                  help="Log file path")
    def main(input_file, output_file, overwrite_output, quiet, distance, log_level, log_filename):
        """A tool to compare given image pairs"""
        config = Config(input_file, output_file, overwrite_output, quiet, distance, log_level, log_filename)
        return image_compare.main(config)



Adding a similarity measurement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming you want to add a new similarity measurement algorithm called `Structural Similarity Index Measure`_ and
there is already a python implementation in the project Skimage_

1) Update our requirements
    Add a new entry to requirements_dev.txt file

    `skimage==0.15.0`

2) Download dependencies

    `python -m pip install -r requirements_dev.txt`

    or

    `python -m pip install skimage==0.15.0`

3) Open `image_compare/similarity.py` file and add our new method
    There are no constraints on the method name but the argument must be a FilePair_ object

    After implementing the body in `image_compare.similarity` module, you should use `@register(name="ssim")`
    and `@TimeSimilarityCalculation` decorators.

    **@register_distance(name)**
        decorator registers your new function as a `similarity_measurement` method and this method will be available
        with `name`'s value e.g.`--distance=ssim` to CLI users without any more code update.

    **@TimeSimilarityCalculation(timing_method=time.perf_counter)**
        decorator times the execution of the method and update the current image pairs `pair.elapsed` member.
        `time.process_time` is used as the default timing method.

        Process_time excludes time elapsed during sleep, if sleep time is important time.perf_counter() can be used.
            See the documentation;

            * process_time: https://docs.python.org/3/library/time.html#time.process_time
            * perf_counter: https://docs.python.org/3/library/time.html#time.perf_counter

    After the completing calculation you must update `pair.similarity`.

    Note: Simplified version showed below for demonstration purposes. You can check the full code here_

..  code-block:: python

    @register_distance(name="ssim")
    @TimeSimilarityCalculation()
    def calculate_ssmi_similarity(pair):
        """Compute the mean structural similarity index between two images.

        :param pair: image pair to compare
        :return:
        """
        image1, image2 = __check_files_and_open(pair)
        img1f = img_as_float(image1)
        img2f = img_as_float(image2)
        similarity = ssim(img1f, img2f, multichannel=True)
        pair.similarity = round(1 - similarity, 3)

4) Add some tests to `tests/test_similarity.py`_ and run them with `python setup.py test`

5) Install the updated version with `python setup.py install` and you can use your new method with;

    `image_compare --distance=ssim input.csv output.csv`

5) That is it. Your new function is ready to use! Please see section about releasing a new version section, if you want to publish your code changes to PyPI.

.. _`Structural Similarity Index Measure`:
.. _Skimage:
.. _FilePair: https://github.com/ggercek/image_compare/blob/master/image_compare/models.py#L4
.. _here: https://github.com/ggercek/image_compare/blob/master/image_compare/similarity.py
.. _`tests/test_similarity.py`: https://github.com/ggercek/image_compare/blob/master/tests/test_similarity.py


Test Data
---------

During development I created a small test data, which can be found under `files/images`_ folder

.. _`files/images`: https://github.com/ggercek/image_compare/tree/master/files/images

I applied some basic manipulation to create variations of the initial images.
Image names contain the manipulation applied on it. Details

* **Box**: Added a solid box 1/16 of the image size
* **Hue**: Maxed out Hue slider on Photoshop
* **CloneStamp**: Mnipulated images with Clone Stamp tool in Photoshop
* **WM-size**: Watermarking image in two sizes as big and small
* **Crop-Left|Right** Cropped %10 of the original image from Left or Right

Here are some sample images:

.. image:: https://github.com/ggercek/image_compare/raw/master/files/images/cat.png
        :alt: cat.png: Cat Original
        :width: 200 px

.. image:: https://github.com/ggercek/image_compare/raw/master/files/images/cat-box.png
        :alt: cat-box.png: Cat Original
        :width: 200 px

.. image:: https://github.com/ggercek/image_compare/raw/master/files/images/cat-clonestamp.png
        :alt: cat-clonestamp.png: Cat Original
        :width: 200 px

.. image:: https://github.com/ggercek/image_compare/raw/master/files/images/cat-hue.png
        :alt: cat-hue.png: Cat Original
        :width: 200 px

.. image:: https://github.com/ggercek/image_compare/raw/master/files/images/cat-wm-small.png
        :alt: cat-wm-small.png: Cat Original
        :width: 200 px

.. image:: https://github.com/ggercek/image_compare/raw/master/files/images/cat-wm-big.png
        :alt: cat-wm-big.png: Cat Original
        :width: 200 px


**Credits for images**

* Toronto Cityscape Photo by Alex Shutin on Unsplash
* Cat Photo by Yerlin Matu on Unsplash
* Nature1 Photo by eberhard grossgasteiger on Unsplash
* Nature2 Photo by Daniel Roe on Unsplash

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
