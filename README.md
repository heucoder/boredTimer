# boredTimer

### **函数运行时间统计工具**

利用装饰器和traceback实现了一个简单的函数运行时间统计工具。

![image](https://github.com/heucoder/boredTimer/blob/main/Lark20201115123332.png)

- 支持如下功能：
  - 支持多个模块之间调用关系

  - 装饰器注册

    ```python
    @BTimer.timethis
    def func3():
        time.sleep(1)
        print("i am util func3 ")
    ```

  - 手动注册

    ```python
    def func2():
        time.sleep(3)
        print("i am util func2")
    
    
    BTimer.register(globals(), func2)
    ```

- 如何使用

  - ```
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
    ```

    - 使用装饰器@BTimer.timethis直接注册函数或者。
    - 在函数运行之前使用BTimer.register()函数注册，务必传入globals()函数。
    - 在所有注册的函数运行结束之后使用BTimer.show()函数即可得到每个函数的运行时间，详细用法详见/example/example.py函数。
