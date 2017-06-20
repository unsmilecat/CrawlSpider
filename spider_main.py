from CrawlSpider_Zhihu import signin, question, people, topic, connect_sql
import re

class SpiderMain(object):
    def __init__(self):
        self.Signin = signin.Signin()
        self.Question =question.Question()
        self.People = people.People()
        self.Topic = topic.Topic()
        self.Connection = connect_sql.Connect()

    def crawl(self):
        account = input('请输入账号：')
        password = input('请输入密码：')
        session = self.Signin.signin(account,password)
        url = input('请输入所需爬取的页面地址：\n')
        if(re.search(r'/question/\d+',url)):
            database = self.Question.get_data(session,url)
        elif(re.search(r'/people/',url)):
            database = self.People.get_data(session,url)
        else:
            database = self.Topic.get_data(session,url)


if __name__=='__main__':
    obj_spider = SpiderMain()
    obj_spider.crawl()