from BoredTimer import BTimer
from util import func3
import time

btime = BTimer()


@btime.timethis
def func1(*k):
    time.sleep(1)
    print("i am func1")


@btime.timethis
def func2():
    func1()
    func1()
    x = 2
    y = 4
    print("i am func2")
    return x+y


@btime.timethis
def func4():
    func2()
    print("i am func4")


if __name__ == "__main__":
    btime.register(globals(), func3, func2, func1, func4)
    # btime.register(globals(), func1, func2, func3)
    print("-"*30)
    func1()
    print("*"*20)
    func2()
    print("*"*20)
    func3()
    print("*"*40)
    func4()
    print("-"*30)
    btime.show()
