import gzip
import re
import urllib
from bs4 import BeautifulSoup as bs
class Topic(object):
    def ungzip(self, data):
        try:
            print('正在解压.....')
            data = gzip.decompress(data)
            print('解压完毕!')
        except:
            print('未经压缩, 无需解压')
        return data

    def get_data(self, s, url):
        agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        headers = {
            'User-Agent': agent
        }
        res = s.get(url, headers=headers)
        soup = bs(self.ungzip(res.text),'html.parser')
        links = soup.find_all('a',class_='question_link')
        questions = list()
        for link in links:
            full_url = urllib.parse.urljoin(url, link['href'])
            question_name = link.get_text()
            questions.append({'url':full_url,'name':question_name})
        return questions
