"""Processing of tasks, core management"""

import os
import importlib.util
from time import sleep
from multiprocessing import Process, Queue, active_children
from queue import Empty

from task import basic_tasks


def run_function(out_queue: Queue, path, function_name, *args):
    """Import and run function from different python files

    :param out_queue: Queue to put respond of function
    :param path: Path to file which contains function
    :param function_name: Name of function to run
    :param args: Arguments to transfer to function
    """
    try:
        spec = importlib.util.spec_from_file_location(function_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        out_queue.put(('Exception during module loading', e))
        return
    try:
        ans = getattr(module, function_name)(*args)
    except Exception as e:
        out_queue.put(('Exception during function execution', e))
        return
    if str(type(ans)) == '<class \'generator\'>':
        for a in ans:
            out_queue.put(a)
    else:
        out_queue.put(ans)


class TaskProcessor:
    """Main object of Assistant core.

    Process all tasks and responds. Execute task's respond when needed. Manage request and responds
    """

    def __init__(self, q_in: Queue, q_out: Queue):
        """Initialize TaskProcessor

        :param q_in: Queue to get input requests
        :param q_out: Queue to put responds
        """
        self.q_in = q_in
        self.q_out = q_out
        self.comp = Queue()
        self.possible_tasks = basic_tasks()
        self.active = True  # Flag for closing
        self.initialize_form_file()
        Process(target=run_function, args=(self.comp, 'Lib/core_functions.py', 'socket_activation', *tuple()),
                name='socket_activation').start()

    def initialize_form_file(self):
        """Run tasks from config file"""
        filename = os.path.join(r'../Assistant_Archive/', 'init_config.txt')
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    self.process_query(line.rstrip())

    def terminate(self):
        """Terminate children processes and stop"""
        children = active_children()
        for ch in children:
            ch.terminate()
        self.active = False

    def run(self):
        """Main loop

        Check input requests and process it.
        Check responds, put them to self.q_out or execute
        """
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
            sleep(0.01)

    def process_query(self, query):
        """Run function which fit query

        :param query: str to process
        """
        for t in self.possible_tasks:
            if t.fit(query):
                Process(target=run_function, args=(self.comp, t.file, t.func_name, *t.eval_p(query)),
                        name=query).start()
                break
