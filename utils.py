import pkg_resources
import os


class Params:
    root_dir = pkg_resources.resource_filename(__name__, ".")
    example_file = os.path.join(root_dir, "./test/gene_report_20190426.xlsx")