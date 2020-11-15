# coding:utf-8
import time

from BoredTimer import BTimer


@BTimer.timethis
def func3():
    time.sleep(1)
    print("i am util func3 ")


def func2():
    time.sleep(3)
    print("i am util func2")


BTimer.register(globals(), func2)
