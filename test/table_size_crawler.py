from urllib import request
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 第8章的网址
    url = 'http://www.poi86.com/poi/amap/district/230102/1.html'
    head = {}
    # 使用代理
    head[
        'User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    req = request.Request(url, headers=head)
    response = request.urlopen(req)
    html = response.read()
    # 创建request对象
    soup = BeautifulSoup(html, 'lxml')
    # 找出div中的内容
    soup_table = soup.find('li',string = "尾页")
    last_idx_link = soup_table.a.attrs['href']
    table_size = last_idx_link[last_idx_link.rfind('/')+1:len(last_idx_link)-5]
    response.close()