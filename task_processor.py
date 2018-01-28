from multiprocessing import Process, Queue, active_children
from queue import Empty
import importlib.util
from task import basic_tasks


def run_function(out_queue, path, function_name, *args):
    spec = importlib.util.spec_from_file_location(function_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    ans = getattr(module, function_name)(*args)
    out_queue.put(ans)


class TaskProcessor:
    def __init__(self, q_in, q_out):
        self.q_in = q_in
        self.q_out = q_out
        # self.processes = []
        self.comp = Queue()
        self.possible_tasks = basic_tasks()

    def run(self):
        while True:
            try:
                while True:
                    s = self.comp.get(block=False)
                    self.q_out.put(s)
            except Empty:
                pass
            try:
                while True:
                    query = self.q_in.get(block=False)
                    if not self.process_query(query):
                        return 0
            except Empty:
                pass

    def process_query(self, query):
        if query in ['exit', 'close', 'выход', 'выйти', 'закрыть']:
            print('exit')
            children = active_children()
            print(children)
            for ch in children:
                ch.terminate()
                print(ch)
            return 0
        else:
            for t in self.possible_tasks:
                if t.fit(query):
                    Process(target=run_function, args=(self.comp, t.file, t.func_name, *t.eval_p(query))).start()
                    break
        return 1
