from xmind2case import handle_xmind_msg, xmind2dict
from write2excel import writr_to_excel


if __name__ == "__main__":
    p = xmind2dict("测试项目投产1.xmind")
    h = handle_xmind_msg(p)
    writr_to_excel("case.xlsx", h)
