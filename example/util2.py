# coding:utf-8
from BoredTimer import BTimer


@BTimer.timethis
def func3():
    print("i am util func3 ")


def func2():
    print("i am util func2")


BTimer.register(globals(), func2)
