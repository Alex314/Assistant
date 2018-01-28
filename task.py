import re


class Task:
    def __init__(self, regex, file_path, name, eval_par):
        self.regex = regex
        self.file = file_path
        self.func_name = name
        self.eval_p = eval_par

    def fit(self, s):
        return re.fullmatch(self.regex, s) is not None


def eval_factorial(regex, s_input):
    gr = re.fullmatch(regex, s_input).groups()
    return int(gr[0]),


def basic_tasks():
    bt = []
    bt += [Task(r'(\d+)!', 'factorial.py', 'factorial', lambda s: eval_factorial(r'(\d+)!', s))]  # Factorial
    bt += [Task(r'[Сс]писок програм|([Ii]nstalled )?[Pp]rograms', 'os_basic.py', 'get_programs', lambda s: tuple())]
    bt += [Task(r'([Зз]апусти(ть)?|[Rr]un) (.*)', 'os_basic.py', 'run_program',
                lambda s: (re.fullmatch(r'([Зз]апусти(ть)?|[Rr]un) (.*)', s).groups()[2],))]
    return bt


if __name__ == '__main__':
    f = Task(r'(\d+)!', 'factorial.py', 'factorial', lambda s: eval_factorial(f.regex, s))
    inp = ['123!', '0!', '-1!', 'a', '!', '14! + 15!']
    for i in inp:
        match = re.fullmatch(f.regex, i)
        print(f.fit(i))
        if f.fit(i):
            print(i, f.eval_p(i))
