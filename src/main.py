import os
import subprocess
from selenium import webdriver
from utils.xlsParser import create_settings


def start_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--dns-prefetch-disable')
    options.add_argument('--no-referrers')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-audio')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    return webdriver.Chrome(options=options)


def create_image(url, name):
    driver.get("http://127.0.0.1:8080/" + url)
    driver.set_window_size(3840, 2160)
    driver.save_screenshot('../results/' + name + '.png')


if __name__ == '__main__':
    op = input('crawl course table from jiaowu ? (y / n) : ')
    if op.lower() == 'y':
        create_settings()
    op = input('start generate ? (y / n) : ')
    if op.lower() != 'y':
        exit(0)
    serve = subprocess.Popen('npm run serve', shell=True)
    driver = start_chrome()
    create_image('', 'index')
    files = filter(lambda x: x.endswith('.jpg'), os.listdir('./assets'))
    names = [i for i in map(lambda x: x[:-4], sorted(files, key=lambda x: (len(x), x)))]
    for i in range(len(names)):
        create_image(names[i], 'pic' + str(i + 1))
        print('image' + names[i] + '.jpg finished, now ' + str(i + 1) + ' / ' + str(len(names)))
    subprocess.Popen('taskkill /f /pid {pid} /t'.format(pid=serve.pid))
    driver.quit()
