import requests
import re
import os
from time import sleep
import winsound


def save_page(adress, filename=None):
    directory = r'../Assistant_Archive/'
    os.makedirs(directory, exist_ok=True)
    if filename is None:
        filename = os.path.join(directory, re.sub(r'[^-\w]+', '_', adress) + '.html')
    with open(filename, 'wb') as fl:
        fl.write(requests.get(adress).content)


def compare_page_to_file(adress, filename=None):
    directory = r'../Assistant_Archive/'
    if filename is None:
        filename = os.path.join(directory, re.sub(r'[^-\w]+', '_', adress) + '.html')
    if not os.path.exists(filename):
        return False
    with open(filename, 'rb') as fl:
        return fl.read() == requests.get(adress).content


def compare_text_page_to_file(adress, filename=None):
    directory = r'../Assistant_Archive/'
    if filename is None:
        filename = os.path.join(directory, re.sub(r'[^-\w]+', '_', adress) + '.html')
    if not os.path.exists(filename):
        return False
    with open(filename, 'r', encoding='utf-8') as fl:
        regex = r'<(style|script)[^>]*>.*?</(\1)>|<[^>]*>'
        old_t = re.sub(regex, ' ', fl.read())
        new_t = re.sub(regex, ' ', requests.get(adress).text)
        regex2 = r'\s+'
        old_t = re.sub(regex2, ' ', old_t)
        new_t = re.sub(regex2, ' ', new_t)
        return old_t == new_t


def str_to_filename(s):
    return re.sub(r'[^-\w]+', '_', s)


def save_link_to_visit(file_to_visit, to_visit):
    if len(to_visit) == 0:
        try:
            os.remove(file_to_visit)
        except FileNotFoundError:
            pass
        return
    with open(file_to_visit + '.tmp', 'w', encoding='utf-8') as f:
        for lnk in to_visit:
            f.write(lnk + '\n')
    try:
        os.remove(file_to_visit)
    except FileNotFoundError:
        pass
    os.rename(file_to_visit + '.tmp', file_to_visit)


def walk_site(adress, beg=None, startswith='', to_visit=set(), visited=set(), file_to_visit='', save_every=200):
    adress = adress.rstrip('/')
    if adress not in visited:
        yield adress
        to_visit.add(adress)
    visited.add(adress)
    if beg is None:
        beg = re.findall(r'[^:]+://[^/]+', adress)[0]
    i = 0
    while len(to_visit) > 0:
        i += 1
        print('Left', len(to_visit))
        link = to_visit.pop()
        visited.add(link)
        if startswith == '':
            startswith = beg
        for ln in parse_links(link, start_with=startswith, beg=beg):
            ln = ln.rstrip('/')
            if ln not in visited:
                if ln not in to_visit:
                    yield ln, len(to_visit)
                to_visit.add(ln)
        if i > save_every and file_to_visit != '':
            save_link_to_visit(file_to_visit, to_visit)
            print('Saved', len(to_visit), 'links to visit')
            i = 0
    if file_to_visit != '':
        save_link_to_visit(file_to_visit, to_visit)


def save_walk(link, filename=None, begin=None, startswith=''):
    if begin is None:
        begin = re.findall(r'[^:]+://[^/]+', link)[0]
    if filename is None:
        filename = str_to_filename(begin) + '.txt'
    file_to_check = filename[:-4] + '.tocheck.txt'
    exists = set()
    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as f:
            for ln in f:
                exists.add(ln.rstrip())
    yield 'Already exists ' + str(len(exists))
    to_check = set()
    if os.path.exists(file_to_check):
        with open(file_to_check, encoding='utf-8') as f:
            for ln in f:
                to_check.add(ln.rstrip())
    yield 'To check ' + str(len(to_check))
    i = 0
    for lnk, left in walk_site(link, begin, startswith=startswith, to_visit=to_check, visited=exists, file_to_visit=file_to_check):
        if i > 499:
            yield 'Have ' + str(len(exists)) + ' Left ' + str(left)
            i = 0
        i += 1
        if lnk not in exists:
            with open(filename, 'a', encoding='utf-8') as f:
                try:
                    f.write(lnk + '\n')
                    exists.add(lnk)
                except UnicodeEncodeError:
                    yield 'UnicodeEncodeError: ' + lnk


def parse_links(adress, start_with='', beg=None, include_adress=False):
    res = requests.get(adress)
    if res.status_code != 200:
        print('Broken page', adress)
        print('Status code', res.status_code)
        return []
    res = res.text
    links = re.findall(r'<a[^>]+href=[\'"]([^>\'"]+)[\'"]', res)
    if beg is None:
        beg = re.findall(r'[^:]+://[^/]+', adress)[0]
    ans = []
    if include_adress:
        ans += [adress]
    for lnk in links:
        if lnk.startswith('//'):
            lnk = beg[:beg.index('://') + 1] + lnk
        if lnk.startswith('/'):
            lnk = beg + lnk
        if lnk.startswith(start_with) and lnk not in ans:
            ans += [lnk]
    return ans


def check_page(url, wait_sec=60):
    directory = r'../Assistant_Archive/'
    filename = os.path.join(directory, re.sub(r'[^-\w]+', '_', url) + '.html')
    if not os.path.exists(filename):
        save_page(url)
    while True:
        if not compare_page_to_file(url):
            yield url + ' changed'
            winsound.PlaySound('Notify.wav', winsound.SND_FILENAME)
            save_page(url)
        sleep(wait_sec)


def check_text_page(url, wait_sec=60):
    directory = r'../Assistant_Archive/'
    filename = os.path.join(directory, re.sub(r'[^-\w]+', '_', url) + '.html')
    if not os.path.exists(filename):
        save_page(url)
    while True:
        if not compare_text_page_to_file(url):
            yield url + ' changed'
            winsound.PlaySound('Notify.wav', winsound.SND_FILENAME)
            save_page(url)
        sleep(wait_sec)


if __name__ == '__main__':
    adres = r'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=f4a70e94-229b-44c9-b777-634a13217f9c'
    adres = r'http://apeps.kpi.ua/'
    #adres = r'http://tef.kpi.ua/'
    # save_page(r'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=f4a70e94-229b-44c9-b777-634a13217f9c', 'rozklad2.html')
    r1 = ''
    r2 = ''
    '''with open('rozklad.html', 'r') as f:
        r1 = f.read()
    with open('rozklad2.html', 'r') as f:
        r2 = f.read()
    print(r1 == r2)
    # print('Total pages:', len(walk_site(adres)))
    a = r'https://github.com/Alex314/Assistant'
    # save_page(a)
    # print(compare_page_to_file(a))
    for i in check_text_page(a):
        print(i)
    compare_text_page_to_file(a, filename=os.path.join(r'../../Assistant_Archive/', re.sub(r'[^-\w]+', '_', a) + '.html'))'''
    fn1 = r'D:\Programming\Python\Assistant\Lib\https_hostelpay_kpi_ua_Pay_Invoices_4R348agW9ip5aUATT0Kewh4xpTQ7wqWVm0yvYvb_2JNyD6XsMo2BC5ZvZkJtHQDrsnuOxnkSW_ - Copy.html'
    fn2 = r'D:\Programming\Python\Assistant\Lib\https_hostelpay_kpi_ua_Pay_Invoices_4R348agW9ip5aUATT0Kewh4xpTQ7wqWVm0yvYvb_2JNyD6XsMo2BC5ZvZkJtHQDrsnuOxnkSW_.html'
    #save_walk(adres)
    adres = r'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=2cbb65b7-fcb3-4c56-9676-69d363997259'
    #save_walk(adres)
    #parse_wiki()
    '''#with open(fn1, 'r', encoding='utf-8') as fl, open(fn2, 'r', encoding='utf-8') as f2:
        regex = r'<(style|script)[^>]*>.*?</(\1)\s*>|<[^>]*(?=<)|<[^>]*>'
        old_t = re.sub(regex, ' ', fl.read())
        new_t = re.sub(regex, ' ', f2.read())
        print(old_t == new_t)
        regex2 = r'\s+'
        old_t = re.sub(regex2, ' ', old_t)
        new_t = re.sub(regex2, ' ', new_t)
        #print(new_t)
        print(old_t == new_t)'''
