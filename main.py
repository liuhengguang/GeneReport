from advice import *
from utils import Params

# ================= #
# output advices
# ================= #
regularized_input = xlsx_read_v3(file_dir=Params.example_input, sheet_name="man_799", min_col=0, max_col=2,
                                 min_row=0, max_row=100)
original_advices, splited_advices, splited_advices_v2, _ = load_knowledge()

# jibing, jibing_high_probability, jibing_high_population, kuangwz, weiss, yesuan, shansdx, personal_features
jibing = [item[0] for item in regularized_input[0:36] if item[1] == 1]
kuangwz = [item[0] for item in regularized_input[38:42] if item[1] == 1]
weiss = [item[0] for item in regularized_input[42:50] if item[1] == 1 and item[0] != "叶酸"]
yesuan = [item[0] for item in regularized_input if item[0] == "叶酸" and item[1] == 1]
shansdx = []

# advices generation
for i in jibing:
    for advice in splited_advices[i]:
        # print(advice)
        pass

final_output_advices, diet_advices = advice_generation(jibing, kuangwz, weiss, yesuan, shansdx, splited_advices, splited_advices_v2)

private_advices = [i[0] for i in final_output_advices if "s" in i[1]]
non_private_advices = [i for i in final_output_advices if type(i) != tuple]

# ================= #
# 疾病建议
# ================= #
diseases_advices = "根据您的遗传基因信息显示，您在:\n    "
diseases = jibing  # 挑选出来的疾病
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




