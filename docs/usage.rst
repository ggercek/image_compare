=====
Usage
=====

If you want to automate or replace the CLI you can create a models.Config and pass it to the image_compare.main(config)
method::

    from image_compare import image_compare
    from image_compare.models import Config

    overwrite_output=False
    quiet=False, distance="ssim"
    quiet=True
    log_level="INFO"
    log_filename="image_compare.log"

    config = Config(input_file, output_file, overwrite_output, quiet, distance, log_level, log_filename)
    exit_code = image_compare.main(config)

    # exit code definitions are under image_compare.ExitCodes
    if exit_code == 0:
        # Success
        pass

If you are not sure which distance methods are supported::

    from image_compare.similarity import get_supported_similarity_methods, get_similarity_measurement

    methods = get_supported_similarity_methods()
    print(methods)

If you want to test different methods on a FilePair object::

    from image_compare.models import FilePair
    from image_compare.similarity import get_supported_similarity_methods, get_similarity_measurement

    FilePair pair = FilePair("image1.png", "image2.png")

    methods = get_supported_similarity_methods()
    for method_name in methods:
        method = get_similarity_measurement(method_name)
        print(method(pair))
        # If you want to use the same file pair object multiple times,
        # initialize the values to avoid possible dirty reads.
        pair.similarities = -1
        pair.elapsed = -1


