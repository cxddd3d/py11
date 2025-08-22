# 作者: 王道 龙哥
# 2025年08月21日15时57分26秒
# xxx@qq.com

import struct

file_name='file.txt'
a=len(file_name.encode('utf-8'))
train_head=struct.pack('I',a)
print(train_head)

#把train_head变为整型对象
b=struct.unpack('I',train_head)
print(b)