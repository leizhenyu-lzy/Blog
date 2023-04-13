def add_str(cls):
    def __str__(self):
        return str(self.__dict__)
    cls.__str__ = __str__  # 重载 __str__ 改变默认 print
    return cls

if __name__ == "__main__":
    @add_str  # 装饰类的装饰器
    class Obj:
        def __init__(self,a,b):
            self.a = a
            self.b = b

    # 等价形式 : Obj = add_str(Obj)  # 直接对类做手脚

    obj = Obj(1,2)  # 类已经被动了手脚，然后才初始化的对象
    print(obj)  # {'a': 1, 'b': 2}


    class Obj:
        def __init__(self,a,b):
            self.a = a
            self.b = b
    obj = Obj(1,2)
    print(obj)  # <__main__.Obj object at 0x7f72198d38e0>