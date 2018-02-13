import re


class Task:
    def __init__(self, regex, file_path, name, eval_par, example):
        self.regex = regex
        self.file = file_path
        self.func_name = name
        self.eval_p = eval_par
        self.example = example

    def fit(self, s):
        return re.fullmatch(self.regex, s) is not None


def eval_factorial(regex, s_input):
    gr = re.fullmatch(regex, s_input).groups()
    return int(gr[0]),


def basic_tasks():
    bt = []
    bt += [Task(r'(\d+)!', 'Lib/factorial.py', 'factorial', lambda s: eval_factorial(r'(\d+)!', s), '{int>=0}!')]
    bt += [Task(r'[Сс]писок программ|([Ii]nstalled )?[Pp]rograms', 'os_basic.py', 'get_programs', lambda s: tuple(),
                'Список программ')]
    bt += [Task(r'([Зз]апусти(ть)?|[Rr]un) (.*)', 'Lib/os_basic.py', 'run_program',
                lambda s: (re.fullmatch(r'([Зз]апусти(ть)?|[Rr]un) (.*)', s).groups()[2],), "Запустить {}")]
    bt += [Task(r'[Сс]писок команд|[Кк]оманды|[Cc]ommands|[Cc]ommand[s] list',
                'Lib/core_functions.py', 'get_command_list', lambda s: tuple(), 'Команды')]
    bt += [Task(r'[Сс]писок процессов|[Пп]роцессы|[Pp]rocess(es)?( list)?',
                'Lib/core_functions.py', 'get_active_processes', lambda s: tuple(), 'Процессы')]
    bt += [Task(r'([Оо]становить процесс|([Tt]erminate|[Kk]ill)( [Pp]rocess)?) (.*)',
                'Lib/core_functions.py', 'terminate_process_by_name',
                lambda s: (re.fullmatch(r'([Оо]становить процесс|([Tt]erminate|[Kk]ill)( [Pp]rocess)?) (.*)', s).groups()[3],),
                'Остановить процесс {}')]
    bt += [Task(r'[Пп]ерезапус(к|тить)|[Rr]estart',
                'Lib/core_functions.py', 'restart', lambda s: tuple(), 'Перезапуск')]
    bt += [Task('[Ee]xit|[Cc]lose|[Вв]ыход|[Вв]ыйти|[Зз]акрыть',
                'Lib/core_functions.py', 'close_app', lambda s: tuple(), 'Выход')]
    bt += [Task(r'([Пп]роверять сайт по тексту|[Cc]heck (web)?site by text) (.*)', 'Lib/net.py', 'check_text_page',
                lambda s: (re.fullmatch(r'([Пп]роверять сайт по тексту|[Cc]heck (web)?site by text) (.*)', s).groups()[2],),
                'Проверять сайт по тексту {}')]
    bt += [Task(r'([Пп]роверять сайт|[Cc]heck (web)?site) (.*)', 'Lib/net.py', 'check_page',
                lambda s: (re.fullmatch(r'([Пп]роверять сайт|[Cc]heck (web)?site) (.*)', s).groups()[2],),
                'Проверять сайт {}')]

    return bt


if __name__ == '__main__':
    f = Task(r'(\d+)!', 'Lib/factorial.py', 'factorial', lambda s: eval_factorial(f.regex, s), '2!')
    inp = ['123!', '0!', '-1!', 'a', '!', '14! + 15!']
    for i in inp:
        match = re.fullmatch(f.regex, i)
        print(f.fit(i))
        if f.fit(i):
            print(i, f.eval_p(i))
