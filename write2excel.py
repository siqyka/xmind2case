import xlwt
from sometools import clock, getConfigs
import json


style = xlwt.XFStyle()
style.alignment.wrap = 1

style1 = xlwt.easyxf('font: bold on,height 220')


def _write_data(sheet, data, index_excel):

    row = 1
    for x in data:
        print(x)
        for k, v in x.items():
            sheet.write(row, index_excel[k], v.replace(
                "\\r\\n", "\\n").strip(), style)
        row += 1


def writr_to_excel(excel_path, xmind_msg):
    wb = xlwt.Workbook()

    sheet1 = wb.add_sheet('测试用例', cell_overwrite_ok=True)

    index_excel = {}
    th = getConfigs().get("th").split(",")

    for i in range(len(th)):
        sheet1.col(i).width = 256*30
        index_excel[th[i]] = i
        sheet1.write(0, i, th[i], style1)
    _write_data(sheet1, xmind_msg, index_excel)
    wb.save(excel_path)


if __name__ == "__main__":
    writr_to_excel(1, 2)
