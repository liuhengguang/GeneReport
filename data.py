from utils import Params
from openpyxl import load_workbook


def xlsx_read(file_dir=Params.example_input, sheet_name="男（799）", min_col=0, max_col=14, min_row=2, max_row=75):
    wb = load_workbook(file_dir)
    sheet = wb[sheet_name]
    # print("===================表格基本信息：=======================")
    # print("sheet names:", wb.sheetnames)
    # print(sheet_name+"的维度：", sheet.calculate_dimension())
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


def get_input(input_excel=Params.example_input, sheet_name="女（799）"):
    input_cols = xlsx_read(file_dir=input_excel, sheet_name=sheet_name)
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

