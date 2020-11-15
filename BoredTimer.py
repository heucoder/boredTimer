# coding:utf-8
import time
from functools import wraps
import traceback

from const import DEFAULT_TREE_DEPTH, MISS_FILE_NAME, MISS_FILE_FUNC


class TimeNode():
    def __init__(self, name=None, start_time=None, end_time=None,
                 dur_time=None, level=None, row=-1,
                 node_id="-1", parent_node_id="-2",
                 belong_file=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.dur_time = dur_time
        self.level = level
        # id
        self.node_id = node_id
        self.row = row
        self.parent_node_id = parent_node_id
        self.belong_file = belong_file
        self.childs = {}

    def id(self):
        return self.node_id

    def parent_id(self):
        return self.parent_node_id

    def append_child(self, timenode):
        self.childs[timenode.id()] = timenode

    def show(self):
        if self.id() == "-1":
            print("Result: ")
        else:
            tab = "    "
            row = self.belong_file + '+' + str(self.row)
            print("%s %s %s:   %s %s %.3f" % (tab*self.level, row,
                                              self.name, self.start_time,
                                              self.end_time,
                                              self.dur_time))

    def iter(self):
        self.show()
        for key in sorted(self.childs.keys()):
            self.childs[key].iter()


class BTimer():
    def __init__(self):
        pass

    root = TimeNode()
    nodes = {root.id(): root}
    func_dict = {}
    tree_depth = DEFAULT_TREE_DEPTH

    @classmethod
    def register(cls, g, *funcs):
        for func in funcs:
            g[func.__name__] = cls.timethis(func)

    @classmethod
    def timethis(cls, func):
        '''
        Decorator that reports the execution time.
        '''
        if cls.func_exists(func):
            return func
        cls._func_add(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            traceback_stack = traceback.extract_stack()
            level, row, node_id, parent_node_id, belong_file =\
                cls._prase_traceback(traceback_stack)
            func_name = cls._get_func_name(func)
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            dur = end - start
            cls._add_nodes(func_name, start, end,
                           dur, level, row, node_id,
                           parent_node_id, belong_file)
            return result
        return wrapper

    @classmethod
    def check(cls):
        for val, item in cls.func_dict.items():
            print("moudle %s: " % val)
            print(item)

    @classmethod
    def show(cls):
        print("*"*50)
        cls._create_tree()
        cls.root.iter()
        print("*"*50)

    @classmethod
    def func_exists(cls, func):
        module_name = func.__module__
        func_name = func.__name__
        module = cls.func_dict.get(module_name, None)
        if module:
            if func_name in module:
                return True
            return False
        return False

    @classmethod
    def _func_add(cls, func):
        if cls.func_exists(func):
            return True
        module_name = func.__module__
        func_name = func.__name__
        module = cls.func_dict.get(module_name, None)
        if module:
            module.append(func_name)
        else:
            cls.func_dict[module_name] = [func_name]
        return True

    @classmethod
    def _add_nodes(cls, func_name, start_time, end_time,
                   dur_time, level, row, node_id, parent_node_id,
                   belong_file):
        if level > cls.tree_depth:
            return
        start_time = cls._timestamp2time(start_time)
        end_time = cls._timestamp2time(end_time)
        tree_node = TimeNode(func_name, start_time, end_time, dur_time,
                             level, row, node_id, parent_node_id, belong_file)
        cls.nodes[tree_node.id()] = tree_node

    @classmethod
    def _prase_traceback(cls, traceback_stack):
        traceback_stack = traceback_stack[::2]
        # print(traceback_stack)
        n = len(traceback_stack)
        level = n - 1
        node_id = cls._get_id(traceback_stack)
        belong_file = traceback_stack[level][0]
        row = int(traceback_stack[level][1])
        parent_node_id = "-1" if level == 0 \
            else cls._get_id(traceback_stack[:-1])
        return level, row, node_id, parent_node_id, belong_file

    @classmethod
    def _miss_traceback(cls, traceback_item):
        if traceback_item[0] == MISS_FILE_NAME and\
           traceback_item[2] == MISS_FILE_FUNC:
            return False
        return True

    @classmethod
    def _create_tree(cls):
        for _, val in cls.nodes.items():
            par_timenode = cls.nodes.get(val.parent_id(), None)
            if par_timenode:
                par_timenode.append_child(val)

    @classmethod
    def _get_func_name(cls, func):
        return func.__name__

    @classmethod
    def _timestamp2time(cls, timestamp):
        time_local = time.localtime(timestamp)
        dt = time.strftime("%H:%M:%S", time_local)
        return dt

    @classmethod
    def _get_id(cls, traceback_stack):
        return "-".join([item[0] + '+' + str(item[1])
                         for item in traceback_stack])


if __name__ == "__main__":
    pass
