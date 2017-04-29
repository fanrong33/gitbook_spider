# encoding: utf-8
# @author 蔡繁荣
# @version 1.0.3 build 20170429
# 解析使用wget下载下来的html文件，下载css,js等静态资源文件，并进行替换链接等操作
# 实现完全的本地化

import sys
import os
import html.parser as h 
from urllib import request
from urllib.parse import urlparse


global g_domain
g_domain = ''

# 解析html文件的静态资源链接
# @param string  html_file   预解析的html文件
# @return list
def parse_assets_link(html_file):

    links = []

    class MyHTMLParser(h.HTMLParser):

        a_t = False

        #处理开始标签，比如<xx>
        def handle_starttag(self, tag, attrs):
            #print("开始一个标签:",tag)

            if str(tag).startswith("title"):
                self.a_t = True

            if tag == 'link':
                for attr in attrs:
                    if attr[0] == 'href':
                        print("属性值：", attr[1])
                        links.append(attr[1])

            if tag == 'script':
                for attr in attrs:
                    if attr[0] == 'src':
                        print("属性值：", attr[1])
                        links.append(attr[1])
           # print()

        #处理<xx>data</xx>中间的那些数据
        def handle_data(self, data):
            pass
            #if self.a_t is True:
            #    print("得到的数据: ",data)
                
        def handle_endtag(self, tag):
            self.a_t=False
            pass
            #print("结束一个标签:",tag)
            #print()

    # 读取已下载文件的内容
    fp = open(html_file, 'r')
    content = fp.read()
    fp.close()

    # 解析html文件得到链接
    p = MyHTMLParser()
    p.feed(content)
    p.close()

    return links


# 下载静态资源
# 在解析的过程在保存g_domain eg: https://example.gitbooks.io/
# @param list  links   要下载的静态资源列表
def download(links):

    # 遍历循环所有的链接，下载需要的静态资源js和css
    for url in links:

        # 解析url得到 domain
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        path = url.replace(domain, '')

        # 得到文件路径和文件名
        new_dir, filename = os.path.split(path)


        lists = ['.js', '.css']
        new_dir2, ext = os.path.splitext(path)
        if ext not in lists:
            continue

        if os.path.exists(new_dir) == False:
            # 循环创建目录
            os.makedirs(new_dir) 

        try:
            # 将抓取的数据直接保存到本地
            result = request.urlretrieve(url, new_dir+"/"+filename)
            print(result)
            # ('baidu.html', <httplib.HTTPMessage instance at 0x10b6b2d40>)
        except Exception as e:
            print(e)
            # [Errno socket error] [Errno 8] nodename nor servname provided, or not known


# 替换html文件内容
def replace_html(html_file, second_domain, book_name, website):

    domain = 'https://%s.gitbooks.io/' % second_domain


    # 1. 'https://example.gitbooks.io/', 全部替换为空
    fp = open(html_file, 'r')
    content = fp.read()
    new_content = content.replace(g_domain, '')
    fp.close()

    fp = open(html_file, 'w')

    # 2. 批量替换html文件中a标签的内容，删除sub_domain路径 !!!
    # <a href="book_name/content/  =>  <a href="
    new_content2 = new_content.replace('<a href="%s/content/' % book_name, '<a href="')

    # 3. 添加内联样式，自定义页面样式
    new_content3 = new_content2 + '''
    <style>
    #book-search-input{ display: none; }
    .book-summary ul.summary li:first-child{ margin-top: 6px; }
    </style>
    '''

    # 4. 替换 gitbook slogan链接为产品官网地址 !!!
    new_content4 = new_content3.replace('https://www.gitbook.com/book/%s/%s' % (second_domain, book_name), website)

    fp = open(html_file, 'w')
    fp.write(new_content4)
    fp.close()



if __name__ == '__main__':
    args = sys.argv
    if len(args) == 4:
        html_file     = args[1]
        second_domain = args[2]
        book_name     = args[3]
        website       = args[4]

        links = parse_assets_link(html_file)
        download(links)

        replace_html(html_file, second_domain, book_name, website)
    else:
        print('must be four arguments. eg: parser.py html_file second_domain  book_name website')



