import os


def get_programs(*, extended=False):
    program_names = []
    paths = []
    tree = os.walk(r'C:\ProgramData\Microsoft\Windows\Start Menu')
    for path, folders, files in tree:
        for i in files:
            if i.endswith('.lnk'):
                program_names += [i[:-4]]
                if extended:
                    paths += [os.path.join(path, i)]
    if len(program_names) == 0:
        return "Не могу найти установленных програм"
    if extended:
        return paths, program_names
    return sorted(program_names)


def run_program(name):
    try:
        paths, progs = get_programs(extended=True)
    except ValueError:
        return "Не могу найти програму {0}".format(name)
    if name in progs:
        os.startfile(paths[progs.index(name)])
        return "{0} запущено".format(name)
    else:
        for i, p in enumerate(progs):
            progs[i] = p.lower()
        if name in progs:
            os.startfile(paths[progs.index(name)])
            return "{0} запущено".format(name)
        else:
            possible = []
            for i, p in enumerate(progs):
                if name in p:
                    possible += [(i, p)]
            ans = "Не могу найти програму {0}".format(name)
            if len(possible) > 0:
                ans += '. Возможно вы ищете:'
            for pos in possible:
                ans += '\n' + pos[1]
            return ans


if __name__ == '__main__':
    programs = get_programs()
    if type(programs) is not str:
        for f in programs:
            print(f)
    print()
    print(run_program('excel 2013'))
