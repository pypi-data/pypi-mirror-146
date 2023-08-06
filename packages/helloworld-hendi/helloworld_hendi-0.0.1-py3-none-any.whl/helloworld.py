def say_hello(name=None):
    if name is None:
        return "Hello"
    else:
        return f"hello,{name}"