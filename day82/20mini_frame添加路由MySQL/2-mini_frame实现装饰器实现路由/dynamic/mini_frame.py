import re

# 装饰器往字典里填数据
URL_FUNC_DICT = dict()


# 装饰器的功能是把路径，函数，放到URL_FUNC_DICT
def route(url):
    def set_func(func):
        # URL_FUNC_DICT["/index.py"] = index
        URL_FUNC_DICT[url] = func  # 改变路径配置字典

        # def call_func(*args, **kwargs):
        #     return func(*args, **kwargs)
        #
        # return call_func  # 不 return，不会替换被装饰函数的入口地址

    return set_func


@route("/index.py")
def index():
    with open("./templates/index.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "哈哈哈哈 这是你的本月名称....."

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content


@route("/center.py")
def center():
    with open("./templates/center.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "这里是从mysql查询出来的数据。。。"

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])

    file_name = env['PATH_INFO']
    # file_name = "/index.py"

    # if file_name == "/index.py":
    #     return index()
    # elif file_name == "/center.py":
    #     return center()
    # else:
    #     return 'Hello World! 我爱你中国....'
    try:
        print(URL_FUNC_DICT)
        func = URL_FUNC_DICT[file_name]
        return func()
    # return URL_FUNC_DICT[file_name]()
    except Exception as ret:
        return "产生了异常：%s" % str(ret)
