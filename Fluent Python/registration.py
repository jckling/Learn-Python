# 保存被 @register 装饰的函数引用
registry = []

# 参数是一个函数
def register(func):
    # 打印被装饰函数
    print('running register(%s)' % func)
    
    # 存入 registry
    registry.append(func)
    
    # 必须返回函数
    return func

@register
def f1():
    print('running f1()')

@register
def f2():
    print('running f2()')

def f3():
    print('running f3()')

def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

# 当作脚本运行时执行
if __name__=='__main__':
    main()