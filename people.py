import re
import gzip
class People(object):
    def ungzip(self, data):
        try:
            print('正在解压.....')
            data = gzip.decompress(data)
            print('解压完毕!')
        except:
            print('未经压缩, 无需解压')
        return data

    def get_data(self, s, url):
        list = re.split(r'/',url)
        name = list[4]
        new_url = 'https://www.zhihu.com/api/v4/members/'+name+'?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge[%3F(type%3Dbest_answerer)].topics'
        agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        headers = {
            'User-Agent': agent
        }
        res = s.get(new_url, headers=headers)
        self.ungzip(res.text)
        data = res.json()
        people = {}
        people['name'] = data['name']
        people['followings'] = data['following_count']
        people['followers'] = data['follower_count']
        people['questions'] = data['question_count']
        people['answers'] = data['answer_count']
        people['voted'] = data['voteup_count']
        people['thanked'] = data['thanked_count']
        people['favorited'] = data['favorited_count']
        edu_list = []
        for edu in data['educations']:
            edu_list.append({'major':edu['major']['name']})
            edu_list.append({'school':edu['school']['name']})
        people['educations'] = edu_list
        addr_list = []
        for addr in data['locations']:
            addr_list.append({'addr':addr['name']})
        people['locations'] = addr_list
        return people


