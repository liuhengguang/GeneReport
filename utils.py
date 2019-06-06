import pkg_resources
import os
import matplotlib

from pylab import *


class Params:
    root_dir = pkg_resources.resource_filename(__name__, ".")
    example_input = os.path.join(root_dir, "./test/example_input.xlsx")  # 输入
    man_and_woman_799_advices = os.path.join(root_dir, "./test/man_and_woman_799_advices.xlsx")  # 知识库
    advices_regularization = os.path.join(root_dir, "./test/advices_regularization.xlsx")  # 知识库


def plt_bar():
    myfont = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/ukai.ttc")
    mpl.rcParams['axes.unicode_minus'] = False
    t = [1, 2, 3]
    y = t
    plt.bar(t, y)
    plt.xticks(t, ('Bill', 'Fred', u'中国'), fontproperties=myfont)
    plt.title(u'matplotlib中文显示测试', fontproperties=myfont)
    plt.xlabel(u'这里是X坐标', fontproperties=myfont)
    plt.ylabel(u'这里是Y坐标', fontproperties=myfont)
    plt.show()


if __name__ == "__main__":
    plt_bar()