import os


def find_link(path):
    files = []
    paths = []
    tree = os.walk(path)
    for path, folders, fl in tree:
        for f in fl:
            if f.endswith('.lnk'):
                yield f[:-4], os.path.join(path, f)


def get_programs(*, extended=False):
    program_names = []
    paths = []
    links = [r'C:\ProgramData\Microsoft\Windows\Start Menu',
             r'C:\Users\Public\Desktop',
             os.path.join(os.environ["HOMEPATH"], "Desktop")]
    for link in links:
        for n, p in find_link(link):
            if n not in program_names:
                program_names += [n]
                paths += [p]
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
    print(run_program('py'))
