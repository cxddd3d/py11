from gevent import monkey
import gevent
import requests  
import time

# 有耗时操作时需要
monkey.patch_all()


def my_downLoad(url):
    print('GET: %s' % url)
    response = requests.get(url)
    data = response.text
    print('%d bytes received from %s.' % (len(data), url))


# 记录开始时间
start_time = time.time()

gevent.joinall([
        gevent.spawn(my_downLoad, 'http://www.cskaoyan.com/forum-279-1.html'),
        gevent.spawn(my_downLoad, 'http://www.cskaoyan.com/'),
        gevent.spawn(my_downLoad, 'http://www.cskaoyan.com/thread-666086-1-1.html'),
])

# 计算并输出总耗时
end_time = time.time()
print('总计耗时: %.2f 秒' % (end_time - start_time))


