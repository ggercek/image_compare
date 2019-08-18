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

CLI tool to compare image similarities.


* Free software: GNU General Public License v3
* Documentation: https://image-compare.readthedocs.io.

.. contents::

This tool is developed for a technical challenge provided by Loblaw Digital.

The aim of the challenge is to develop a tool to automate an image similarity comparison process.
The tool consumes a csv input file which represents image pairs on each row, and produces a csv output file
that contains image pair as well as elapsed time and similarity score in range of [0, 1].
0 means identical, 1 means different

Important Considerations and Answers
------------------------------------

Here are the important consideration provided by the challenge document;

* How do you know if your code works?
    * The data and method was not available for this assignment, and the description said
      `"Bjorn is entrusting you to figure out and appropriate scoring algorithm"`.
      I decided to create a small data set, and test multiple image similarity computation methods and fine tune them.
      For more information, please see the `Testing Methods` section
* How are you going to teach Bjorn how to use program?
    * To start with, a one-on-one session would be ideal, but the documentation might be a good start as well.
      In addition to the documentation, the tool handles exceptions properly, and provides descriptive error messages
      to help user to solve their technical problems.
* Your manager Jeanie is assigning you to a different task and is making Ferris the maintainer of your application.
  How do you make sure he succeeds?
    * Both high-level and code-level documentation is available for the project.
    * Unit tests provide guidance about how to use API
    * Under `Development` section two entries can be found as step by step guides to add new functionality.
        * Adding a commandline argument
        * Adding a similarity measurement
    * Automated build and checks will also reduce the on boarding costs & learning curve.
* How are you ensuring Bjorn gets the latest version of your application?
    * Bjorn can install the program by using pip following method::

        pip install image_compare

    * Tool is tested both on Windows and Linux(Ubuntu) and is working without any issues.
    * More information can be found at the `Installation`_ section

.. _`Installation`: https://image-compare.readthedocs.io/en/latest/installation.html

Approach
---------------------------

I used following steps while implementing this tool

* Looked for image similarity methods -
    * Initially came across with SSIM and MSE. They seem popular especially in research papers but I wasn't sure about the application specific data set.
    * So kept looking and found Distance Hash and Perception Hash methods and the imagehash library
    * Used all of these methods to have flexibility while dealing with new data sets.
* Looked for best practices and inspect popular python projects like Requests, Httpie, etc.
    * Setup the plan for project structure and CI flow
    * Used CookieCutterPython template to initialize the project
    * Setup Travis CI
* Aimed for an extendable design as the requirements can be changes over time, and the maintaning
    * Followed an iterative development model: Test -> Code -> Refactor, you can check the git history.
    * Split the code base into multiple modules based on simple responsibilities, to increase readability.
* After implementing initial similarity methods, decided to implement decorators.
    * Although they increase complexity at first, with good documentation and samples, they hide the details while
      improving expressiveness of the code.
    * Implemented decorators for timing and registration of similarity methods
    * Created extra documentation for adding a new similarity method to demonstrate how to use those decorators.
* Implemented exception handling and logging with descriptive messages for users and developers.
* Implemented documentation


How to use
----------
.. code-block::

    Usage: image_compare [OPTIONS] INPUT_FILE OUTPUT_FILE

      A tool to compare given image pairs

    Options:
      --overwrite-output              Overwrite the output if already exists
                                      [default: False]
      --quiet                         Suppress console output  [default: False]
      --distance [ssim|nrmse|dhash|avghash|phash|whash]
                                      Similarity method to compare image pairs
                                      [default: ssim]
      --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                      Log level to control the output volume
                                      [default: INFO]
      --log-filename TEXT             Log file path  [default: image_compare.log]
      --help                          Show this message and exit.


Sample Commands::

    # use default options
    image_compare files/product-cat-photos.csv files/product-cat-photos.csv

    # use dhash
    image_compare --distance=dhash files/product-cat-photos.csv files/product-cat-photos.csv

    # use whash and overwrite output
    image_compare --distance=whash --overwrite-output files/product-cat-photos.csv files/product-cat-photos.csv

    # use ssim and use my_log_file.log as logging, and no console output
    image_compare --distance=ssim --log-filename="my_log_file.log" --quiet \
        files/product-cat-photos.csv files/product-cat-photos.csv

If you want to learn how to use image_compare programmatically please see the `Usage Section`_

.. _`Usage Section`: https://image-compare.readthedocs.io/en/latest/usage.html

Features
--------

* Currently supports only CSV input/output formats

* Supports multiple comparision methods, namely;
    * SSIM: Structural Similarity Index: https://en.wikipedia.org/wiki/Structural_similarity
    * NRMSE: Normalized Root Mean Square Error: https://en.wikipedia.org/wiki/Root-mean-square_deviation#Normalized_root-mean-square_deviation
    * DHash: Difference Hashing: http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html
    * AvgHash: Average Hashing: http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    * PHash: Perception Hashing: http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    * WHash: Wavelet Hashing: https://fullstackml.com/2016/07/02/wavelet-image-hash-in-python/

* The tool has following convenient features as well;
    * Can log to file and console
    * Can suppress console output, useful for automation
    * Provides summary at the end of execution
    * Descriptive error handling: in case of an error tool provides feedback to user about possible solution
    * If an error occurs during the output file creation, the calculated distances will be written to log file.

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
* coverage==4.5.4 -> Test Coverage
* Sphinx==2.1.2 -> Automated documentation generation
* twine==1.13.0
* bandit==1.6.2 -> Static security analyzer


Test Coverage
-------------

Due to technical problems the Coveralls.io integration is not working properly, but the html reports are stored under
`coverage_html_report`_ folder. Also, you can click here_ to see the report online.

(Will update this section, when solving the integration issue)

To generate test coverage on your local installation run::

    coverage run setup.py test
    coverage html

.. _`coverage_html_report`: https://github.com/ggercek/image_compare/tree/master/coverage_html_report
.. _`here`: http://htmlpreview.github.io/?https://raw.githubusercontent.com/ggercek/image_compare/master/coverage_html_report/index.html

Development
-----------

Implementation Details
^^^^^^^^^^^^^^^^^^^^^^

**Modules**

Here is brief description of each module and their components. Also, you can find more info at `Module Index`_

* cli
    Contains Command Line Interface(CLI) definition and help text.
    This module parses user's input and creates a `models.Config` object to pass it
    to `image_compare.main(config)` method.
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
    Please see the `Adding a new similarity measurement` section for implementation details
    Supported methods are : SSIM, NRMSE, DHash, AHash, WHash, PHash.
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

    After completing calculation you must update `pair.similarity`.

    Note: Simplified version showed below for demonstration purposes. You can check the full code at `image_compare/similarity.py`_

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

5) That is it. Your new function is ready to use! Please see section about releasing a new version section,
    if you want to publish your code changes to PyPI.

.. _`Structural Similarity Index Measure`:
.. _Skimage:
.. _FilePair: https://github.com/ggercek/image_compare/blob/master/image_compare/models.py#L4
.. _`image_compare/similarity.py`: https://github.com/ggercek/image_compare/blob/master/image_compare/similarity.py
.. _`tests/test_similarity.py`: https://github.com/ggercek/image_compare/blob/master/tests/test_similarity.py

PyPI Release Checklist
^^^^^^^^^^^^^^^^^^^^^^

(Forked from: `Audreyr's PyPI Checklist`_)

- [ ] Update HISTORY.rst
- [ ] Commit the changes:

::

    git add HISTORY.rst
    git commit -m "Changelog for upcoming release 0.1.1."

- [ ] Update version number (can also be minor or major)

::

    Bump2version patch

- [ ] Install the package again for local development, but with the new version number:

::

    python setup.py develop

- [ ] Run the tests:

::

    tox

- [ ] Release on PyPI by uploading both sdist and wheel:

::

    python setup.py sdist upload
    python setup.py bdist_wheel upload

- [ ] Test that it pip installs:

::

    mktmpenv
    pip install my_project
    <try out my_project>
    deactivate

- [ ] Push: `git push --follow-tags`
- [ ] Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.

.. _`Audreyr's PyPI Checklist`: https://gist.githubusercontent.com/audreyr/5990987/raw/685db574ea2a1a0350dceae53c1fb2b30c16aa94/pypi-release-checklist.md


Test Data
---------

During development I created a small test data, which can be found under `files/images`_ folder

.. _`files/images`: https://github.com/ggercek/image_compare/tree/master/files/images

I applied some basic manipulation to create variations of the initial images.
Image names contain the manipulation applied on it. Details

* **Box**: Added a solid box 1/16 of the image size
* **Hue**: Maxed out Hue slider on Photoshop
* **CloneStamp**: Manipulated images with Clone Stamp tool in Photoshop
* **WM-size**: Watermarked image in two sizes as big and small
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


Simple Test Results
-------------------

2 test scenarios are implemented and discussed briefly.

1) Original Image Comparision
    * **Description**
        * In a simplistic manner, to test similarity methods 4 original images compared against each other.
        * Definition of different images heavily depend on application and context. Colors, composition and other aspects
          should be taken into consideration, but such details require a more in-depth research and prototyping, and it is
          outside scope of this technical challenge.
        * As the definition of difference is not clear in the technical challenge document, I decided to add multiple
          similarity functions, to deal with the unknown data sets.
    * **Results**
        * Files are under `files/evaluation/`_ :
            compare_originals_results_hashsize_8.csv, compare_originals_results_hashsize_16.csv
        * Half of the evaluations are omitted, as they have different sizes. Those rows have a value of
          -1 for similarity and elapsed time columns
        * None of the algorithms managed to produce a similarity value of 1. This requires a threshold value
          calculation based on the application or context requirements.
            * For example, while using DHash a value of 0.5+ can be interpreted as different but that requires at least
              one fine tuning session with sample data sets.
        * In this test, WHash generates lowest scores while comparing nature pictures.


.. csv-table:: Internal Category Comparision with HashSize=8 Detection Numbers
   :header: image1,image2,dhash,avghash,phash,whash,nrmse,ssim
   :widths: auto

    cat.png,cat.png,0,0,0,0,0,0
    cityscape.png,cityscape.png,0,0,0,0,0,0
    nature-1.png,nature-1.png,0,0,0,0,0,0
    nature-2.png,nature-2.png,0,0,0,0,0,0
    cat.png,cityscape.png,0.516,0.469,0.469,0.438,0.532,0.4
    cityscape.png,cat.png,0.516,0.469,0.469,0.438,0.476,0.4
    nature-1.png,nature-2.png,0.562,0.219,0.531,0.188,0.52,0.38
    nature-2.png,nature-1.png,0.562,0.219,0.531,0.188,0.45,0.38


.. csv-table:: Internal Category Comparision with HashSize=16 Detection Numbers
   :header: image1,image2,dhash,avghash,phash,whash,nrmse,ssim
   :widths: auto

    image1,image2,dhash,avghash,phash,whash,nrmse,ssim
    cat.png,cat.png,0,0,0,0,0,0
    cityscape.png,cityscape.png,0,0,0,0,0,0
    nature-1.png,nature-1.png,0,0,0,0,0,0
    nature-2.png,nature-2.png,0,0,0,0,0,0
    cat.png,cityscape.png,0.461,0.457,0.555,0.453,0.532,0.4
    cityscape.png,cat.png,0.461,0.457,0.555,0.453,0.476,0.4
    nature-1.png,nature-2.png,0.465,0.281,0.492,0.273,0.52,0.38
    nature-2.png,nature-1.png,0.465,0.281,0.492,0.273,0.45,0.38



2) Internal Category Comparision
    * **Description**
        * Based on the original images, 4 categories created. Each category contains 1 original image and its variations.
          The variations are defined in previous section.
        * The aim of this scenario is to test the methods capability to detect small changes on images.
        * Applied variations introduce no more than %30 changes to the original images.
        * In addition to categories, 4 Hash Sizes are used for testing, 8, 16, 32, 64. The hash size only applies
          to AHash, DHash, PHash and WHash methods. During testing hash_size values higher than 16 generated
          quite a bit of noise, so they are not included.
            * Note: Hash size values do not affect the results of SSIM and NRMSE
        * The cartesian product of category members are used to generate image pairs for the data set.
          Cartesian product ensured existence of every combination in data set, including the identical pairs.
        * The data set is composed of 27 identical and 162 non-identical pairs

    * **Result**
        * Evaluation results are stored in `files/evaluation/`_ :
          compare_originals_results_hashsize_8.csv, compare_originals_results_hashsize_16.csv
        * HashSize=8 generated False Positives values, due to the lack of details in the final hash values.
            * See the tables below `Internal Category Comparision with HashSize=8`
              and `Internal Category Comparision with HashSize=8 Detection Numbers`
        * HashSize=16 improved results for DHash and PHash to an optimal state within the given data set while
          PHash and WHash still suffers from False Positives.
            * See the tables below `Internal Category Comparision with HashSize=16`
              and `Internal Category Comparision with HashSize=16 Detection Numbers`
        * It is not feasible to create general statements about similarity methods with such a small data set.
        Under given circumstances, DHash and PHash seems more better candidates compare to PHash and WHash. As
        future work, fine tuning of PHash and WHash should be studied.
        * **SSIM** and **NRMSE** both managed to detect all identical files.
            * SSIM is more resistant to changes and the similarity score closer to zero.
            * NRMSE is more agressive and sensitive to small changes.


.. csv-table:: Internal Category Comparision with HashSize=8 Detection Numbers
   :header: "","actual","dhash","avghash","phash","whash","nrmse","ssim"
   :widths: auto

    "identical",27,37,57,31,67,27,27
    "non-identical",162,152,132,158,122,162,162


.. csv-table:: Internal Category Comparision with HashSize=8
   :header: "","dhash","avghash","phash","whash","nrmse","ssim"
   :widths: auto

    "max",0.281,0.359,0.438,0.375,0.396,0.168
    "min",0,0,0,0,0,0
    "stddev",0.070443203,0.087345191,0.119002107,0.099554587,0.106300916,0.049045266
    "median",0.062,0.031,0.094,0.031,0.122,0.036
    "avg",0.074761905,0.06194709,0.133195767,0.072973545,0.141878307,0.054412698


.. csv-table:: Internal Category Comparision with HashSize=16
   :header: "","dhash","avghash","phash","whash","nrmse","ssim"
   :widths: auto

    "max",0.23,0.258,0.453,0.273,0.396,0.168
    "min",0,0,0,0,0,0
    "stddev",0.048071689,0.062382791,0.11597915,0.068472441,0.106300916,0.049045266
    "median",0.062,0.035,0.109,0.047,0.122,0.036
    "avg",0.064867725,0.052550265,0.142148148,0.066698413,0.141878307,0.054412698


.. csv-table:: Internal Category Comparision with HashSize=16 Detection Numbers
   :header: "","actual","dhash","avghash","phash","whash","nrmse","ssim"
   :widths: auto

    "identical", 27, 27, 45, 27, 37, 27, 27
    "non-identical",162,162,144,162,152,162,162


.. _`files/evaluation/`: https://github.com/ggercek/image_compare/tree/master/files/evaluation


Discussion
^^^^^^^^

After initial evaluation,

    * SSIM: Good for detecting big differences, resistant to small changes.
    * NRMSE: Good for detecting small changes especially if color is important (hue changes), the only problem is the
      results are not symmetrical, meaning nrmse(image1, image2) is not equal to nrmse(image2, image1), it generates
      pretty close results, but needs further study.
    * Dhash and PHash are good measurements
    * WHash: good for detecting similar color schemes
    * Need more study about PHash and AvgHash


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
