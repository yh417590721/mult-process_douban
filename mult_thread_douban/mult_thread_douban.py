import json
import threading
import time
from urllib.parse import urlencode

import requests


class taskThread(threading.Thread):
    def __init__(self, threadID, keyword):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.keyword = keyword

    def run(self):
        global overTask
        params = {
            'q': self.keyword,
            'limit': 20,
            'start': (self.threadID - 1) * 20
        }
        url = 'https://www.douban.com/j/search_photo?' + urlencode(params)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            array = parsed_json['images']
            for a in array:
                self.download(a['src'])
            overTask.append(self.threadID)

    def download(self, url):
        # print('download 被调用')
        global number
        global threadLock
        ir = requests.get(url, stream=True)
        filename = str.split(url, '/')
        if ir.status_code == 200:
            threadLock.acquire()
            number = number + 1
            #print('线程' + str(self.threadID) + '--开始写入第' + str(number) + "张" + filename[len(filename) - 1])
            with open(filename[len(filename) - 1], 'wb') as f:
                for chunk in ir:
                    f.write(chunk)
            f.close()
            print('线程' + str(self.threadID) + '--成功写入第' + str(number) + "张")
            threadLock.release()

#-----main-------

# 线程数
thread_num = 10
# 关键字
keyword = '电影'

beginTime = time.time()
threads = []
overTask = []
number = 0
threadLock = threading.Lock()
useTime = 0
t_name = thread_num

while t_name > 0:
    threads.append(taskThread(t_name, keyword))
    t_name = t_name - 1

for t in threads:
    print('开始线程：' + str(t.threadID))
    t.start()

for t in threads:
    t.join()

print('线程结束')