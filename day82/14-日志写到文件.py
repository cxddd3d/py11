# 作者: 王道 龙哥
# 2025年08月29日16时33分26秒
# xxx@qq.com
import logging

logging.basicConfig(level=logging.WARNING,
                    filename='./log.txt',
                    filemode='w',
                    encoding='utf-8',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# use logging
logging.info('这是 loggging info message')
logging.debug('这是 loggging debug message')
logging.warning('这是 loggging a warning message')
logging.error('这是 an loggging error message')
logging.critical('这是 loggging critical message')