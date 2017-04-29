## gitbook_spider

有时候可能需要将在线文档发布为自己的域名

假设我们的gitbook地址为
https://[username].gitbooks.io/example/content/api.html

first
wget -c -r -np -k -L -p https://[username].gitbooks.io/example/content/api.html


-parser.py  html_file  second_domain  book_name  website
parser.py api.html  lilei  example  https://www.example.com