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


def walk_site(adress, beg=None):
    visited = [adress]
    if beg is None:
        beg = re.findall(r'[^:]+://[^/]+', adress)[0]
    to_visit = set()
    to_visit.add(adress)
    while len(to_visit) > 0:
        link = to_visit.pop()
        print(link)
        print('Left', len(to_visit))
        visited += [link]
        for l in parse_links(link, start_with=beg, beg=beg):
            if l not in visited:
                to_visit.add(l)
    return visited


def parse_links(adress, start_with='', beg=None):
    res = requests.get(adress).text
    links = re.findall(r'<a[^>]+href=[\'"]([^>\'"]+)[\'"]', res)
    if beg is None:
        beg = re.findall(r'[^:]+://[^/]+', adress)[0]
    ans = []
    for lnk in links:
        if lnk.startswith('/'):
            lnk = beg + lnk
        if lnk.startswith(start_with) and lnk not in ans:
            ans += [lnk]
    return ans


def check_page(url, wait_sec=5):
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


def check_text_page(url, wait_sec=5):
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
    # save_page(r'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=f4a70e94-229b-44c9-b777-634a13217f9c', 'rozklad2.html')
    r1 = ''
    r2 = ''
    '''with open('rozklad.html', 'r') as f:
        r1 = f.read()
    with open('rozklad2.html', 'r') as f:
        r2 = f.read()
    print(r1 == r2)'''
    # print('Total pages:', len(walk_site(adres)))
    a = r'https://github.com/Alex314/Assistant'
    #save_page(a)
    #print(compare_page_to_file(a))
    for i in check_text_page(a):
        print(i)
    compare_text_page_to_file(a, filename=os.path.join(r'../../Assistant_Archive/', re.sub(r'[^-\w]+', '_', a) + '.html'))
    #print(re.sub(r'[^-\w]+', '_', a) + '.html')
