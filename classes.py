class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        print(self.i)
        return 'hello world'

x = MyClass()

test = x.f()
print(test)