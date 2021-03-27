import time
import functools
import configparser

FMT = "[{t1:0.8f}s] {name}({arg_str}) --> {res}"


def clock(fmt=FMT):
    '''
    一个计算函数执行多少时间的装饰器,
    默认打印--->[执行时间] 函数(参数) --> 返回值,
    param:格式化字符串,格式化字符串可用参数t1(程序用时)、name(程序名)、arg_str(参数)、res(返回值)
    '''
    def decorate(fnc):
        @functools.wraps(fnc)
        def clocked(*args, **kwargs):
            t0 = time.time()
            _res = fnc(*args, **kwargs)
            res = repr(_res)
            t1 = time.time()-t0
            name = fnc.__name__
            arg_list = []
            if args:
                arg_list.append(','.join(repr(arg) for arg in args))
            if kwargs:
                pairs = ['{}:{}'.format(k, w)
                         for k, w in sorted(kwargs.items())]
            arg_str = ",".join(arg_list)
            print(FMT.format(**locals()))
        return clocked
    return decorate


def getConfigs():
    '''
    获取configs.ini配置
    '''
    config = configparser.ConfigParser()
    config.read("configs.ini", encoding="utf-8")
    configD = {}
    for i in config.sections():
        configD.update({k: v for k, v in config.items(i)})
    return configD


if __name__ == "__main__":
    conf = getConfigs()
    print(conf)
