from multiprocessing import Process, Queue, active_children
from queue import Empty
import importlib.util
from task import basic_tasks


def run_function(out_queue, path, function_name, *args):
    spec = importlib.util.spec_from_file_location(function_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    ans = getattr(module, function_name)(*args)
    if str(type(ans)) == '<class \'generator\'>':
        out_queue.put('generator output from {0}'.format(function_name))
        for a in ans:
            put_to_gui(out_queue, a)
    else:
        put_to_gui(out_queue, ans)


def put_to_gui(queue, arg):
    queue.put(arg)


class TaskProcessor:
    def __init__(self, q_in, q_out):
        self.q_in = q_in
        self.q_out = q_out
        # self.processes = []
        self.comp = Queue()
        self.possible_tasks = basic_tasks()

        # Flag for closing
        self.active = True

    def terminate(self):
        children = active_children()
        for ch in children:
            ch.terminate()
        self.active = False

    def run(self):
        while self.active:
            try:
                while self.active:
                    s = self.comp.get(block=False)
                    try:
                        if len(s) == 2 and s[0] == 'exec':
                            exec(s[1])
                        else:
                            self.q_out.put(s)
                    except TypeError:
                        self.q_out.put(s)
            except Empty:
                pass
            try:
                while self.active:
                    query = self.q_in.get(block=False)
                    self.process_query(query)
            except Empty:
                pass

    def process_query(self, query):
        for t in self.possible_tasks:
            if t.fit(query):
                Process(target=run_function, args=(self.comp, t.file, t.func_name, *t.eval_p(query)), name=query).start()
                break
