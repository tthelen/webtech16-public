

def enterexit(f):
    def wrap():
        print("Enter '{}'".format(f.__name__))
        f()
        print("Exit '{}'".format(f.__name__))
    return wrap


def log(enter, exit):
    def enterexit(f):
        def wrap():
            if enter:
                print("Enter '{}'".format(f.__name__))
            f()
            if exit:
                print("Exit '{}'".format(f.__name__))
        return wrap
    return enterexit


@enterexit
def helloworld():
    print("Hello world.")


@log(True, False)
def helloworld2():
    print("Hello world2!")

helloworld()
helloworld2()
