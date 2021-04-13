registry = set()  # <1>

# 装饰器工厂函数
def register(active=True):
    
    # 装饰器
    def decorate(func):
        print('running register(active=%s)->decorate(%s)'
              % (active, func))
        if active:   # 闭包
            registry.add(func)
        else:
            registry.discard(func)

        return func  # 装饰器返回函数
    return decorate  # 装饰器工厂函数返回 decorate

# 必须作为函数调用，并传入所需参数
@register(active=False)
def f1():
    print('running f1()')

# 关键字参数默认值
@register()
def f2():
    print('running f2()')

# 无装饰器
def f3():
    print('running f3()')