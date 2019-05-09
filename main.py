from utils import Params
from openpyxl import load_workbook
from advice_db.advice_db import *


def xlsx_read(file_dir=Params.example_file, sheet_name="男（799）", min_col=0, max_col=14, min_row=2, max_row=75):
    wb = load_workbook(file_dir)
    sheet = wb[sheet_name]
    # print("===================表格基本信息：=======================")
    # print("sheet names:", wb.sheetnames)
    print(sheet_name+"的维度：", sheet.calculate_dimension())
    r = sheet.calculate_dimension()
    data = sheet[r.split(":")[0][0]+":"+r.split(":")[1][0]]
    if max_row >= int(r.split(":")[1][1:]):
        max_row = int(r.split(":")[1][1:])
    total = []
    for col in range(min_col, max_col):  # 列
        temp = []
        for row in range(min_row, max_row):  # 行
            # print(data[row][col].value)
            temp.append(data[col][row].value)
        # print(temp)
        total.append(temp)
    # print(total)
    return total


def get_input():
    input_cols = xlsx_read(sheet_name="男（799）")
    # a exp line in total_rows: (1, '骨科疾病', '骨关节炎', 0.609499828501506, 8.868, 14.5497, 2, None)]
    input_rows = list(zip(input_cols[0],
                          input_cols[1],
                          input_cols[2],
                          input_cols[6],
                          input_cols[7],
                          input_cols[9],
                          input_cols[12],
                          input_cols[13]
                          ))
    return input_cols, input_rows


def selecting_results():
    """
    从所有检测项目中挑出我们关注的项
    :return:
    """
    input_cols, input_rows = get_input()

    jibing_high_p = [i for i in input_rows
                     if i[0] == 1 and i[4] >= 10]
    jibing_high_population = [i for i in input_rows
                              if i[0] == 1 and i[3] >= 2 and i[4] <= 10]
    jibing = jibing_high_p + jibing_high_population

    kuangwz = [i for i in input_rows
               if i[1] == "矿物质" and "高" in i[-1]]

    weiss = [i[2] for i in input_rows
             if i[1] == "维生素" and i[2] != "叶酸" and "高" in i[-1]]

    yesuan = [i[2] for i in input_rows
              if i[2] == "叶酸" and "高" in i[-1]]

    shansdx = [i for i in input_rows
               if i[1] == "膳食代谢" and ("高" in i[-1] or "浅尝" in i[-1] or "戒酒" in i[-1] or "小酌" in i[-1] or "不耐受" in i[-1])]

    personal_features = [i for i in input_rows
                         if i[0] == 3]

    return jibing, kuangwz, weiss, yesuan, shansdx, personal_features


# ========================= #
# advices
# ========================= #
jibing, kuangwz, weiss, yesuan, shansdx, personal_features =  selecting_results()
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


# ====================== #
# step3: load knowledge
# ====================== #
def knowledge():
    """
    :return: original_advices; splited_advices; splited_advices_v2; splited_advices_descriptions
    """
    advices_cols = xlsx_read(Params.man_and_woman_799_advices, sheet_name="man_and_woman_799", max_col=3, min_row=1, max_row=1000)
    knowledge_rows = list(zip(advices_cols[1], advices_cols[2]))
    cnt = 0
    cnt2 = 0
    diseases = []
    diseases2 = []
    original_advices = dict()  # 原始建议
    splited_advices = dict()  # 分词结果
    label = False
    label2 = False
    if knowledge_rows[-1] != ("end", "end"):
        knowledge_rows.append(("end", "end"))
    for row in knowledge_rows:
        d = row[0]
        if "#" in d:
            temp = []
            label = True
            cnt = cnt + 1
            d = d[1:]
            d = d.replace(" ", "")
            diseases.append(d)
            # print(d)
        if label and "分词结果" in row[0]:
            # print(diseases[cnt-1])
            label = False
            original_advices[diseases[cnt-1]] = temp
        if label and "(" in row[0]:
            temp.append(row[0])

        if "分词结果" in d:
            temp2 = []
            label2 = True
            cnt2 = cnt2 + 1
            continue
            # print(d)
        if label2 and ("#" in row[0] or "end" in row[0]):
            # print(diseases[cnt-2])
            label2 = False
            splited_advices[diseases[cnt-2]] = temp2
        if label2:
            temp2.append((row[0], row[1]))

    # 建议描述
    splited_advices_descriptions = []
    for key in splited_advices.keys():
        for row in splited_advices[key]:
            splited_advices_descriptions.append(row[1])
            # print(row[1])
    splited_advices_descriptions = set(splited_advices_descriptions)  # 去处重复
    splited_advices_v2 = dict()
    for row in splited_advices_descriptions:
        temp = []
        for key in splited_advices.keys():
            for row1 in splited_advices[key]:
                if row1[1] == row:
                    temp.append(row1[0])
        splited_advices_v2[row] = temp
    return original_advices, splited_advices, splited_advices_v2, splited_advices_descriptions


original_advices, splited_advices, splited_advices_v2, _ = knowledge()

# ================= #
# output advices
# ================= #
output_advices = []
for row in jibing:
    print(row[2], ":")
    for advice in splited_advices[row[2]]:
        output_advices.append(advice)
        print("    ", advice[0])

# merging output advices
final_output_advices = []
for row in output_advices:
    if "s" in row[1]:
        final_output_advices.append(row)
        output_advices.remove(row)
idx = [i[1] for i in output_advices]
idx = set(idx)
for row in idx:
    advice = splited_advices_v2[row][0]
    final_output_advices.append(advice)

# for row in diet_advices:
#     print(row)


