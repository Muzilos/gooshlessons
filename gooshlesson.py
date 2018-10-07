
from bs4 import BeautifulSoup as bsoup

import os
import urllib2
import requests
import time
import argparse

BASE_PATH = os.getcwd()
MAGOOSH_DIR = BASE_PATH + '/MagooshVideos'

MATH_DIR = MAGOOSH_DIR +'/Math'
VERBAL_DIR = MAGOOSH_DIR + '/Verbal'
WRITING_DIR = MAGOOSH_DIR + '/Writing'

MATH_LINK_LIST = ['https://gre.magoosh.com/lessons/1390-intro-to-gre-math', 'https://gre.magoosh.com/lessons/1185-properties-of-real-numbers',
                  'https://gre.magoosh.com/lessons/1227-intro-to-percents',
            'https://gre.magoosh.com/lessons/106-divisibility',
            'https://gre.magoosh.com/lessons/35-intro-to-algebra', 'https://gre.magoosh.com/lessons/70-intro-to-word-problems',
            'https://gre.magoosh.com/lessons/21-intro-to-exponents', 'https://gre.magoosh.com/lessons/91-lines-and-angles',
            'https://gre.magoosh.com/lessons/61-the-coordinate-plane', 'https://gre.magoosh.com/lessons/121-mean-median-mode',
            'https://gre.magoosh.com/lessons/126-introduction-to-counting', 'https://gre.magoosh.com/lessons/137-intro-to-probability',
            'https://gre.magoosh.com/lessons/900-intro-to-data-interpretation', 'https://gre.magoosh.com/lessons/1398-qc-questions-inequalities',
            ]

VERBAL_LINK_LIST = ['https://gre.magoosh.com/lessons/149-intro-to-text-completion', 'https://gre.magoosh.com/lessons/155-intro-to-no-shift-sentences',
                    'https://gre.magoosh.com/lessons/159-intro-to-sentence-shifts', 'https://gre.magoosh.com/lessons/164-intro-to-double-blank-sentences',
                    'https://gre.magoosh.com/lessons/169-intro-to-triple-blank-sentences', 'https://gre.magoosh.com/lessons/180-intro-to-sentence-equivalence',
                    'https://gre.magoosh.com/lessons/951-intro-to-vocabulary', 'https://gre.magoosh.com/lessons/1475-intro-to-reading-comprehension',
                    'https://gre.magoosh.com/lessons/994-elements-of-the-argument'
                    ]
WRITING_LINK_LIST = ['https://gre.magoosh.com/lessons/520-intro-to-awa', 'https://gre.magoosh.com/lessons/521-intro-to-issue-task',
                     'https://gre.magoosh.com/lessons/523-intro-to-argument-task'
                     ]

FINAL_LIST = [MATH_LINK_LIST, VERBAL_LINK_LIST, WRITING_LINK_LIST]

def download(url, file_name):
    file_name = file_name.encode('utf-8')
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()


def go_to_path_and_work(argument):
    print argument
    if argument == 'verbal':
        os.chdir(VERBAL_DIR)
        parse_and_download(VERBAL_LINK_LIST, VERBAL_DIR)
        print("--- Completed Verbal Section. Enjoy! and All the Best for GRE ---")

    elif argument == 'math':
        os.chdir(MATH_DIR)
        parse_and_download(MATH_LINK_LIST, MATH_DIR)
        print("--- Completed Math Section. Enjoy! and All the Best for GRE ---")
    elif argument == 'writing':
        os.chdir(WRITING_DIR)
        parse_and_download(WRITING_LINK_LIST, WRITING_DIR)
        print("--- Completed Writing Section. Enjoy! and All the Best for GRE ---")
    elif argument == 'all':
        os.chdir(VERBAL_DIR)
        parse_and_download(VERBAL_LINK_LIST, VERBAL_DIR)
        print("--- Completed Verbal Section --- Starting Math Section after 10 seconds")
        time.sleep(10)
        os.chdir(MATH_DIR)
        parse_and_download(MATH_LINK_LIST, MATH_DIR)
        print("--- Completed Math and Verbal Section --- Starting Writing Section after 10 seconds")
        time.sleep(10)
        os.chdir(WRITING_DIR)
        parse_and_download(WRITING_LINK_LIST, WRITING_DIR)
        print("--- Completed all 3 Sections Enjoy! and All the Best for GRE ---")

def parse_and_download(url_list, dir):
    for url in url_list:
        source = requests.get(url).text
        magoosh_soup = bsoup(source, "html.parser")
        lesson_list = magoosh_soup.find_all('ul', attrs={"class": "lesson-list"})[1]

        lesson_list_to_proc = lesson_list.find_all('div', attrs={'class': 'lesson-item'})
        # enabled_lesson_list = lesson_list.find_all('div', attrs={'class': 'lesson-item'})
        # print len(set(enabled_lesson_list))
        # print len(set(disabled_lesson_list))
        # print len(set(disabled_lesson_list).intersection(set(enabled_lesson_list)))

        process_list(lesson_list_to_proc, dir)
        # process_list(enabled_lesson_list)

def process_list(proc_list, dir):
    extension = "/web_webm.webm"

    for lesson in proc_list:
        img = lesson.find('img')
        title = lesson.find('h3', attrs={'class': 'lesson-item-title'}).text
        file_name = title + ".webm"
        file_path = dir + '/' + file_name
        link = '/'.join(img['src'].split('/')[:-1])
        final_link = link + extension
        if not os.path.isfile(file_path):
            download(final_link, file_name)
            time.sleep(5)


def make_dirs():

    if not os.path.exists(MAGOOSH_DIR):
        os.mkdir(MAGOOSH_DIR)

    os.chdir(MAGOOSH_DIR)
    if not os.path.exists(MATH_DIR):
        os.mkdir(MATH_DIR)

    if not os.path.exists(VERBAL_DIR):
        os.mkdir(VERBAL_DIR)
    if not os.path.exists(WRITING_DIR):
        os.mkdir(WRITING_DIR)

if __name__ == '__main__':
    make_dirs()

    parser = argparse.ArgumentParser(description='Provide which section you want to download!')
    parser.add_argument('-s', '--section', help='Provide which section you want to download math/verbal/writing/all')
    argument = parser.parse_args()

    go_to_path_and_work(argument.section)

