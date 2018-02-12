import requests
import re
import os


def save_page(adress, filename=None):
    directory = r'../../Assistant_Archive/'
    if filename is None:
        filename = os.path.join(directory, re.sub(r'[^-\w]+', '_', adress) + '.html')
    with open(filename, 'wb') as fl:
        fl.write(requests.get(adress).content)


def compare_page_to_file(adress, filename=None):
    directory = r'../../Assistant_Archive/'
    if filename is None:
        filename = os.path.join(directory, re.sub(r'[^-\w]+', '_', adress) + '.html')
    with open(filename, 'rb') as fl:
        return fl.read() == requests.get(adress).content


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


if __name__ == '__main__':
    adres = r'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=f4a70e94-229b-44c9-b777-634a13217f9c'
    adres = r'http://apeps.kpi.ua/'
    adres = r'http://xtf.kpi.ua/?q=ru'
    adres = r'http://kfh.kpi.ua/ru/'
    # save_page(r'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=f4a70e94-229b-44c9-b777-634a13217f9c', 'rozklad2.html')
    r1 = ''
    r2 = ''
    '''with open('rozklad.html', 'r') as f:
        r1 = f.read()
    with open('rozklad2.html', 'r') as f:
        r2 = f.read()
    print(r1 == r2)'''
    # print('Total pages:', len(walk_site(adres)))
    a = r'https://www.timeanddate.com/worldclock/ukraine/kyiv'
    os.makedirs(directory, exist_ok=True)
    save_page(a)
    print(compare_page_to_file(a))
    print(re.sub(r'[^-\w]+', '_', a) + '.html')
