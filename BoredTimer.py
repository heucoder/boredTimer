# coding:utf-8
import time
from functools import wraps
import traceback


class TimeNode():
    def __init__(self, name=None, start_time=None, end_time=None,
                 dur_time=None, level=None, row=-1, 
                 node_id="-1", parent_node_id=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.dur_time = dur_time
        self.level = level
        # id
        self.node_id = node_id
        self.row = row
        self.parent_node_id = parent_node_id
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
            print("%s %s %s:   %s %s %.3f" % (tab*self.level, self.row,
                                              self.name, self.start_time,
                                              self.end_time,
                                              self.dur_time))

    def iter(self):
        self.show()
        for key in sorted(self.childs.keys()):
            self.childs[key].iter()


class BTimer():
    def __init__(self, tree_depth=2):
        self.root = TimeNode()
        self.nodes = {self.root.id(): self.root}
        self.funcs = []
        self.tree_depth = tree_depth

    def register(self, g, *funcs):
        for func in funcs:
            g[func.__name__] = self.timethis(func)

    def timethis(self, func):
        '''
        Decorator that reports the execution time.
        '''
        if func.__name__ in self.funcs:
            return func
        self.funcs.append(func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            traceback_stack = traceback.extract_stack()
            level, row, node_id, parent_node_id =\
                self._prase_traceback(traceback_stack)
            func_name = self._get_func_name(func)
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            dur = end - start
            self._add_nodes(func_name, start, end,
                            dur, level, row, node_id,
                            parent_node_id)
            return result
        return wrapper

    def show(self):
        print("*"*50)
        self._create_tree()
        self.root.iter()
        print("*"*50)

    def _add_nodes(self, func_name, start_time, end_time,
                   dur_time, level, row, node_id, parent_node_id):
        if level > self.tree_depth:
            return
        start_time = self._timestamp2time(start_time)
        end_time = self._timestamp2time(end_time)
        tree_node = TimeNode(func_name, start_time, end_time, dur_time,
                             level, row, node_id, parent_node_id)
        self.nodes[tree_node.id()] = tree_node

    def _prase_traceback(self, traceback_stack):
        traceback_stack = traceback_stack[::2]
        n = len(traceback_stack)
        level = n - 1
        node_id = self._get_id(traceback_stack)
        row = int(traceback_stack[level][1])
        parent_node_id = "-1" if level == 0 \
            else self._get_id(traceback_stack[:-1])
        return level, row, node_id, parent_node_id

    def _create_tree(self):
        for _, val in self.nodes.items():
            par_timenode = self.nodes.get(val.parent_id(), None)
            if par_timenode:
                par_timenode.append_child(val)

    def _get_func_name(self, func):
        return func.__name__

    def _timestamp2time(self, timestamp):
        time_local = time.localtime(timestamp)
        dt = time.strftime("%H:%M:%S", time_local)
        return dt

    def _get_id(self, traceback_stack):
        return "-".join([str(item[1]) for item in traceback_stack])


if __name__ == "__main__":
    pass