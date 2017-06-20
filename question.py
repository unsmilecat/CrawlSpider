import sys
import io
import gzip
import re

class Question(object):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    def ungzip(self, data):
        try:
            print('正在解压.....')
            data = gzip.decompress(data)
            print('解压完毕!')
        except:
            print('未经压缩, 无需解压')
        return data

    def get_data(self, s, url):
        id = re.search(r'\d+', url).group(0)
        new_url =  'https://www.zhihu.com/api/v4/questions/'+str(id)+'/answers?include=data%5B*%5D.is_normal%2Cis_collapsed%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20&sort_by=default'
        agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        headers = {
            'User-Agent': agent
        }
        res = s.get(new_url, headers=headers)
        self.ungzip(res.text)
        data = res.json()
        answers_list = []
        while (True):
            ans_list = data['data']
            for ans in ans_list:
                name = ans['author']['name']
                vote = ans['voteup_count']
                content = ans['content']
                answers_list.append({'name':name,'vote':vote,'content':content})
            if (data['paging']['is_end'] == True):
                break
            new_url = data['paging']['next']
            res = s.get(new_url, headers=headers)
            data = res.json()
        return answers_list
