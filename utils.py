import pkg_resources
import os


class Params:
    root_dir = pkg_resources.resource_filename(__name__, ".")
    example_file = os.path.join(root_dir, "./test/gene_report_20190426.xlsx")
    advices_relation = os.path.join(root_dir, "./test/拆分后各项建议关联分析.xlsx")
    man_and_woman_799_advices = os.path.join(root_dir, "./test/man_and_woman_799_advices.xlsx")

