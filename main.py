from utils import Params
from openpyxl import load_workbook
from advice_db.advice_db import *


def xlsx_read(file_dir=Params.example_file, sheet_name="男（799）"):
    wb = load_workbook(file_dir)
    sheet = wb[sheet_name]
    # print("===================表格基本信息：=======================")
    # print("sheet names:", wb.sheetnames)
    # print("男（799）的维度：", sheet.calculate_dimension())
    data = sheet['A:N']
    total = []
    for col in range(0, 14):  # 列
        temp = []
        for row in range(2, 75):  # 行
            # print(data[row][col].value)
            temp.append(data[col][row].value)
        # print(temp)
        total.append(temp)
    # print(total)
    return total


# ======================================== #
# main
# ======================================== #
total_cols = xlsx_read(sheet_name="男（799）")
# a exp line in total_rows: (1, '骨科疾病', '骨关节炎', 0.609499828501506, 8.868, 14.5497, 2, None)]
total_rows = list(zip(total_cols[0],
                      total_cols[1],
                      total_cols[2],
                      total_cols[6],
                      total_cols[7],
                      total_cols[9],
                      total_cols[12],
                      total_cols[13]
                      ))

# ================= #
# step1: selecting results
# ================= #
"""
内分泌系统疾病
妇科疾病
循环系统疾病
泌尿系统疾病
消化系统疾病
神经系统疾病
肿瘤
骨科疾病

"""
jibing_high_p = [i for i in total_rows
                 if i[0] == 1 and i[4] >= 10]
jibing_high_population = [i for i in total_rows
                          if i[0] == 1 and i[3] >= 2 and i[4] <= 10]
jibing = jibing_high_p + jibing_high_population

kuangwz = [i for i in total_rows
           if i[1] == "矿物质" and "高" in i[-1]]

weiss = [i[2] for i in total_rows
         if i[1] == "维生素" and i[2] != "叶酸" and "高" in i[-1]]

yesuan = [i[2] for i in total_rows
          if i[2] == "叶酸" and "高" in i[-1]]

shansdx = [i for i in total_rows
           if i[1] == "膳食代谢" and ("高" in i[-1] or "浅尝" in i[-1] or "戒酒" in i[-1] or "小酌" in i[-1] or "不耐受" in i[-1])]

personal_features = [i for i in total_rows
                     if i[0] == 3]
# ========================= #
# step2: advices
# ========================= #
diet_advices = []

# 矿物质相关建议
if kuangwz:
    for i in kuangwz:
        temp = kwz_advice_db[i[2]]
        diet_advices.append(temp)
        # print(temp)

# 维生素相关建议
if weiss:
    label_B = False
    label_other = False
    other = []
    for i in weiss:
        if "B" in i:
            label_B = True
        elif "B" not in i and weiss:
            other.append(i)
            label_other = True

    if label_B and label_other:
        cnt = 0
        for v in other:
            if cnt == 0:
                vitamin_advice_db["B族和其他"] = vitamin_advice_db["B族和其他"] + other[cnt]
            else:
                vitamin_advice_db["B族和其他"] = vitamin_advice_db["B族和其他"] + "、" + other[cnt]
            cnt = cnt + 1
        diet_advices.append(vitamin_advice_db["B族和其他"])
        # print(vitamin_advice_db["B族和其他"])
    elif label_other and not label_B:
        cnt = 0
        for v in other:
            if cnt == 0:
                vitamin_advice_db["仅其他"] = vitamin_advice_db["仅其他"] + other[cnt]
            else:
                vitamin_advice_db["仅其他"] = vitamin_advice_db["仅其他"] + "、" + other[cnt]
            cnt = cnt + 1
        diet_advices.append(vitamin_advice_db["仅其他"])
        # print(vitamin_advice_db["仅其他"])
    elif not label_other and label_B:
        diet_advices.append(vitamin_advice_db["仅B族"])
        # print(vitamin_advice_db["仅B族"])
    else:
        print("None")
        pass

# 叶酸相关建议
if yesuan:
    diet_advices.append(vitamin_advice_db[yesuan[0]])

# 膳食代谢
for i in shansdx:
    if "乳糖" in i:
        diet_advices.append(rut[i[2]])
    # 脂肪酸和膳食纤维
    if "高" in i:
        diet_advices.append(shansxw[i[2]])
    if "酒精" in i:
        diet_advices.append(jiuj[i[2]])
    if "咖啡因" in i:
        diet_advices.append(kafy[i[2]])

# 运动建议
personal_sport_features = []
for i in personal_features:
    if i[1] == "运动能力":
        personal_sport_features.append(i)



