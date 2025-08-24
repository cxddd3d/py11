import requests  
import time



def my_downLoad(url):
    print('GET: %s' % url)
    response = requests.get(url)
    data = response.text
    print('%d bytes received from %s.' % (len(data), url))
# 不使用协程，逐步访问URL并统计时间
def sequential_download():
    start_time = time.time()
    urls = [
        'http://www.cskaoyan.com/forum-279-1.html',
        'http://www.cskaoyan.com/',
        'http://www.cskaoyan.com/thread-666086-1-1.html'
    ]
    
    print("\n===== 不使用协程，顺序下载 =====")


    
    # 逐个访问URL
    for url in urls:
        my_downLoad(url)
    
    # 计算并输出总耗时
    end_time = time.time()
    print('顺序下载总计耗时: %.2f 秒' % (end_time - start_time))

# 执行顺序下载
sequential_download()