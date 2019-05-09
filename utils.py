import pkg_resources
import os


class Params:
    root_dir = pkg_resources.resource_filename(__name__, ".")
    example_input = os.path.join(root_dir, "./test/gene_report_20190426.xlsx")  # 输入
    man_and_woman_799_advices = os.path.join(root_dir, "./test/man_and_woman_799_advices.xlsx")  # 知识库

