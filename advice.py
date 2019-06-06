from advice_db.advice_db import *
from data import *


def load_knowledge():
    """
    step3: load knowledge
    :return: original_advices; splited_advices; splited_advices_v2; splited_advices_descriptions
    """
    advices_cols = xlsx_read(Params.man_and_woman_799_advices,
                             sheet_name="man_and_woman_799", max_col=3, min_row=1, max_row=1000)
    knowledge_rows = list(zip(advices_cols[1], advices_cols[2]))
    cnt = 0
    cnt2 = 0
    diseases = []
    # 原始建议
    original_advices = dict()
    # 分词结果
    splited_advices = dict()
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
    # 以“建议描述”为key
    splited_advices_v2 = dict()
    for row in splited_advices_descriptions:
        temp = []
        for key in splited_advices.keys():
            for row1 in splited_advices[key]:
                if row1[1] == row:
                    temp.append(row1[0])
        splited_advices_v2[row] = temp
    return original_advices, splited_advices, splited_advices_v2, splited_advices_descriptions


def advice_generation(jibing, kuangwz, weiss, yesuan, shansdx, splited_advices, splited_advices_v2):
    # 仅仅根据疾病得出的初始建议（疾病对应的建议应该优先级最高?）
    output_advices = []
    # 存储最终建议
    final_output_advices = []
    for row in jibing:
        for advice in splited_advices[row]:
            output_advices.append(advice)
    # 先加入各个疾病的私有建议(建议描述为"s")
    for row in output_advices:
        if "s" in row[1]:
            final_output_advices.append(row)
            output_advices.remove(row)
    # 对非私有建议中的“建议描述”去重
    idx = [i[1] for i in output_advices]
    idx = list(set(idx))
    # 解决非私有建议与膳食建议中的冲突(暂时考虑以下几组冲突)：
    # 蛋白质：多蛋白质，少蛋白质； todo
    # 维生素：多维生素C；
    # 酒精：戒酒、限酒；
    # 铁：多铁；
    # 膳食纤维：多膳食纤维；
    # 钙：避免过度补钙, 补钙; todo
    for i in idx:
        if "多维生素C" in i:
            weiss.append("维生素C")
            idx.remove(i)
        if "铁" in i:
            kuangwz.append("铁")
            idx.remove(i)
        if "酒" in i:
            shansdx.append(i)
            idx.remove(i)
    weiss = list(set(weiss))
    kuangwz = list(set(kuangwz))
    shansdx = list(set(shansdx))
    for row in idx:
        # 非私有建议可能存在同一个“建议描述”对应着多条意思相同或相近的建议，现暂时指定第一条，后续可考虑引入随机性
        advice = splited_advices_v2[row][0]
        final_output_advices.append(advice)

    # =================== #
    # 膳食相关建议
    # =================== #
    diet_advices = []
    # 矿物质相关建议
    if kuangwz:
        for i in kuangwz:
            temp = kwz_advice_db[i]
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

    # 膳食代谢相关建议
    label_jiejiu = False
    label_xianjiu = False
    for i in shansdx:
        if "乳糖" in i:
            diet_advices.append(rut[i])
        # 脂肪酸和膳食纤维
        if "膳食纤维" in i:
            diet_advices.append(shansxw[i])
        if "戒酒" in i:
            label_jiejiu = True
        if "限酒" in i:
            label_xianjiu = True
        if "咖啡因" in i:
            diet_advices.append(kafy["咖啡因"])
    if label_jiejiu and label_xianjiu:
        diet_advices.append(jiuj["酒精"]["戒酒"])
    elif not label_jiejiu and label_xianjiu:
        diet_advices.append(jiuj["酒精"]["限酒"])
    else:
        pass

    return final_output_advices, diet_advices


if __name__ == "__main__":
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

    final_advices, diet_advices = advice_generation(jibing, kuangwz, weiss, yesuan, shansdx)