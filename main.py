from advice import *
from utils import Params

# ================= #
# output advices
# ================= #
jibing_high_probability, jibing_high_population, final_output_advices, diet_advices = \
    advice_generation(input_excel=Params.example_input, sheet_name="女（799）")
private_advices = [i[0] for i in final_output_advices if "s" in i[1]]
non_private_advices = [i for i in final_output_advices if type(i) != tuple]

# ================= #
# 疾病建议
# ================= #
diseases_advices = "根据您的遗传基因信息显示，您在:\n    "
jibing_high_probability = [i[2] for i in jibing_high_probability]
jibing_high_population = [i[2] for i in jibing_high_population]
diseases = jibing_high_probability + jibing_high_population  # 挑选出来的疾病
for i in range(len(diseases)):
    if i == 0:
        diseases_advices = diseases_advices + diseases[0]
    else:
        diseases_advices = diseases_advices + "、" + diseases[i]
diseases_advices = diseases_advices + "的患病概率较大\n您平时的体检需要特别注意以下内容:\n"
tijian = "    318 套餐\n    798 套餐\n    1198 套餐\n    1899 套餐\n    3298 套餐\n    (根据相关系数确定定制套餐内容)\n\n"
diseases_advices = diseases_advices + tijian
print(diseases_advices)

print("\n为了您的健康，我们给出一些建议供您参考：")

for i in private_advices:
    print("    ", i)
print("\n")
for i in non_private_advices:
    print("    ", i)
print("\n")
for i in diet_advices:
    print("    ", i)

print("\n\n(另外,如果您对具体某项遗传信息比较感兴趣需要了解更多内容, 建议您可以通过目录查找,如“高血压”在第 39 页.)")




