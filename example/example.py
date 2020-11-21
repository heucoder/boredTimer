# coding:utf-8
import sys
import time
sys.path.insert(0, "../")
sys.path.insert(0, '.')

from BoredTimer import BTimer
from util2 import func3
from util1 import func33


# @BTimer.timethis
def func1(*k):
    time.sleep(1)
    print("i am func1")


@BTimer.timethis
def func2():
    func1()
    func1()
    x = 2
    y = 4
    print("i am func2")
    return x+y


def func4():
    time.sleep(1.3)
    func2()
    print("i am func4")


if __name__ == "__main__":
    BTimer.register(globals(), func33, func2, func1, func4)
    print("-"*30)
    func1()
    print("*"*20)
    func2()
    print("*"*20)
    func3()
    print("*"*20)
    func33()
    print("*"*40)
    func4()
    print("-"*30)
    BTimer.check()
    BTimer.show()
    # for i in dir(func1.__code__):
    #     if i.startswith("co"):
    #         print(i+":", eval("func1.__code__."+i))