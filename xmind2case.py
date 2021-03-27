from sometools import clock, getConfigs
from xmindparser import xmind_to_dict
import collections
import ast


def _analysisXmind(root, str_root, alist):
    '''

    '''
    if isinstance(root, dict):
        if len(root) >= 2 and "topics" in root.keys():
            if str_root == "":
                str_root = root["title"]
            _analysisXmind(root["topics"], str(str_root), alist)

        elif len(root) == 1:
            _analysisXmind(root["title"], str(str_root), alist)

        else:
            case_dict = {}
            case_dict["note"] = root["note"]
            case_dict["case_path"] = str(str_root)
            alist.append(case_dict)
    elif isinstance(root, list):
        for r in root:
            _analysisXmind(r, str(str_root)+"/"+r["title"], alist)
    elif isinstance(root, str):
        case_dict = {}
        case_dict["note"] = ""
        case_dict["case_path"] = str(str_root)
        alist.append(case_dict)


def xmind2dict(xmind_path):
    xdict = xmind_to_dict(xmind_path)
    print(xdict)
    root = xdict[0]["topic"]
    # print(root)
    path_list = []
    _analysisXmind(root, "", path_list)
    return path_list


def handle_xmind_msg(xmsgdict):
    conf = ast.literal_eval(getConfigs().get("xe"))
    confl = [x for x in collections.OrderedDict(conf).keys()]
    case_msg_list = []
    for xd in xmsgdict:
        case_fdict = {}
        note = xd.setdefault("note", "")

        if note == "":
            case_fdict["路径"] = xd["case_path"]
            case_path_list = xd["case_path"].split("/")

            try:
                case_fdict[conf.get("测试名称")] = "_".join(case_path_list[-4:])
            except:
                case_fdict[conf.get("测试名称")] = "_".join(case_path_list)
            case_msg_list.append(case_fdict)
            continue

        for k in range(len(confl)-1):
            start_str, end_str = confl[k], confl[k+1]

            index1, index2 = note.find(start_str), note.find(end_str)
            if index1 == -1:
                if start_str == "路径":
                    case_fdict[conf[start_str]] = xd["case_path"]
                elif start_str == "测试名称":
                    case_path_list = xd["case_path"].split("/")
                    try:
                        case_fdict[conf[start_str]] = "_".join(
                            case_path_list[-4:])
                    except:
                        case_fdict[conf[start_str]] = "_".join(case_path_list)
                else:
                    print("请检查配置文件XcorrespondE配置项XE字典的第{}个key[{}]是否在xmind各个最后节点的备注中！".format(
                        k+1, start_str))
                    # pass
            elif k == len(confl)-2:
                # 出来当key是最后倒数两项的时候
                case_fdict[conf[start_str]] = note[index1 +
                                                   len(start_str)+1:index2]
                case_fdict[conf[end_str]] = note[index2+len(end_str)+1:]

            else:
                case_fdict[conf[start_str]] = note[index1 +
                                                   len(start_str)+1:index2]
        case_msg_list.append(case_fdict)
    return case_msg_list


if __name__ == "__main__":
    p = xmind2dict("测试项目投产1.xmind")
    h = handle_xmind_msg(p)
    print(h)
