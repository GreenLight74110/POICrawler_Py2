from urllib import request
from bs4 import BeautifulSoup
import time
import sys

if __name__ == '__main__':
    # 第8章的网址
    url = 'http://www.poi86.com/poi/amap/district/230102/1.html'
    head = {}
    # 使用代理
    head[
        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    req = request.Request(url, headers=head)
    response = request.urlopen(req)
    html = response.read()
    # 创建request对象
    soup = BeautifulSoup(html, 'lxml')

    soup_table_end = soup.find('li', string="尾页")
    last_idx_link = soup_table_end.a.attrs['href']
    table_size = int(last_idx_link[last_idx_link.rfind('/') + 1:len(last_idx_link) - 5])

    # 打开文件
    if(len(sys.argv)) > 2:
        f = open(sys.argv[1], 'w')
        f_log = open(sys.argv[2], 'w')

        for i in range(1, table_size):
            table_url = 'http://www.poi86.com/poi/amap/district/230102/' + str(i) + '.html'
            # 遇到exception重发10次
            for attemp_i in range(10):
                try:
                    # do some logic
                    table_req = request.Request(table_url, headers=head)
                    table_response = request.urlopen(table_req)
                    table_html = table_response.read()
                    table_soup = BeautifulSoup(table_html, 'lxml')

                    # 找出表格中的条目
                    table_trs = table_soup.find_all('tr')

                    for j in range(1, table_trs.__len__()):
                        # do some logic
                        soup_tr = table_trs[j]

                        results = []
                        tr_name = soup_tr.td.text
                        results.append(tr_name)
                        tr_link = 'http://www.poi86.com' + soup_tr.td.a.attrs['href']
                        results.append(tr_link)

                        # 遇到exception重发10次
                        for attemp_j in range(10):
                            try:
                                detail_req = request.Request(tr_link, headers=head)
                                detail_response = request.urlopen(detail_req)
                                detail_html = detail_response.read()
                                detail_soup = BeautifulSoup(detail_html, 'lxml')

                                detail_items = detail_soup.find_all('li', class_='list-group-item')

                                for k in range(0, 3):
                                    results.append(detail_items[k].a.text)
                                for k in range(3, 9):
                                    results.append(detail_items[k].contents[1].strip())

                                results_str = ''
                                for item in results:
                                    results_str += item + "\t"
                                f.write(results_str + "\n")

                                detail_response.close()
                            except Exception as e:
                                if attemp_j >= 9:
                                    # do_some_log()
                                    f_log.write("item " + str(j) + " in page " + str(i) + " skipped : \n" + e+"\n")
                                else:
                                    time.sleep(0.5)
                            else:
                                f_log.write("item " + str(j) + " in page " + str(i) + " finished.\n")
                                time.sleep(0.1)
                                break

                    table_response.close()
                except Exception as e:
                    if attemp_i >= 9:
                        # do_some_log()
                        f_log.write("page " + str(i) + " skipped : " + e+"\n")
                    else:
                        time.sleep(0.5)
                else:
                    f_log.write("**********page " + str(i) + " finished.\n**********")
                    f.flush()
                    f_log.flush()
                    time.sleep(0.1)
                    break

        f.flush()
        f_log.flush()
        f.close()
        f_log.close()

