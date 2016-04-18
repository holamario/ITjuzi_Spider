import urllib.request as fetch
import urllib.parse as parse
import re
from pymongo import MongoClient as mc
from time import sleep
import random



def investmentevent(i):
    '''#headers = {'Host': 'www.itjuzi.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',

               'Referer': 'https://www.itjuzi.com/investevents',
               'Cookie': '_ga=GA1.2.565573215.1460770455; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1460770457,1460968932; gr_user_id=934aa765-ef6f-41ac-85f0-5ed7697a9428; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1460981087; session=1ab25d5e7ce2f8d256fe88548290da14f493ae6c; _gat=1; gr_session_id_eee5a46c52000d401f969f4535bdaa78=ce0b592b-20e5-4683-b3ed-ffd6a3f326ec',
               'Connection': 'keep-alive'}'''

    url = 'https://www.itjuzi.com/investevents?page=' + str(i)

    #req=fetch.Request(url,headers=headers)
    #response = fetch.urlopen(req)
    response = fetch.urlopen(url)
    response = response.read().decode('utf8')

    pattern = re.compile('<ul class="list-main-eventset">(.*?)</ul>', re.S)
    results = re.findall(pattern, response)
    results = results[0].replace('\t', '').replace('\n', '')
    pattern2 = re.compile('<li>(.*?)</li>')
    results2 = re.findall(pattern2, results)
    events = []
    for each in results2:
        investment_event = {}

        # p_date=re.compile('<i class="cell round"><span>(.*?)</span></i>')
        # date=re.findall(p_date,each)[0]

        p1 = re.compile(
            '<i class="cell round"><span>(.*?)</span></i><i class="cell pic">.*?</i><i class="cell maincell"><p class="title"><a target="_blank" href="(.*?)"><span>(.*?)</span></a></p><p><span class="tags t-small c-gray-aset"><a href="(.*?)">(.*?)</a></span><span class="loca c-gray-aset t-small"><a href="(.*?)">(.*?)</a></span></p></i><i class="cell round"><a><span class="tag gray">(.*?)</span></a></i><i class="cell fina">(.*?)</i><i class="cell date"><span class="investorset">(.*?)</span></i>')
        basic_info = {}
        r1 = re.findall(p1, each)
        if r1:
            r1 = r1[0]
            # print(r1)
            if (r1):
                basic_info['time'] = r1[0]
                basic_info['event_id'] = r1[1]
                basic_info['company'] = r1[2].replace('.', '_')
                basic_info['category_url'] = r1[3]
                basic_info['category'] = r1[4]
                basic_info['location_url'] = r1[5]
                basic_info['location'] = r1[6]
                basic_info['round'] = r1[7]
                basic_info['quantity'] = r1[8]
            # print(r1)
            investment_event['basic_info'] = basic_info
            investors = {}
            p2_1 = re.compile('<a target="_blank" href="(.*?)">(.*?)</a>')
            r2_1 = re.findall(p2_1, r1[9])

            if r2_1:
                for each_investor in r2_1:
                    investors[each_investor[1].replace('.', "_")] = each_investor[0]
            p2_2 = re.compile('<span class="c-gray">(.*?)</span>')
            r2_2 = re.findall(p2_2, r1[9])

            if r2_2:
                for each_investor in r2_2:
                    investors[each_investor.replace('.', "_")] = 'none'
            investment_event['investment_info'] = investors

            # print(investment_event)
            events.append(investment_event)
        else:
            with open('missed', 'a') as out:
                out.write(str(i) + '\n')
    return events



def main_action():
    client = mc()
    db = client.ITjuzi
    tobecaptured = db.ToBeCaptured
    pages = tobecaptured.find({'done': 0})
    number = pages.count()
    events = db.InvestmentEvent
    for page in pages:
        time = 3 * random.random()
        sleep(time)
        pageid = page['pageid']
        print('now fetching page ' + str(pageid))
        data = investmentevent(pageid)
        for each in data:
            print(each)
            events.insert_one({'data': each})
        tobecaptured.update_one({'pageid': pageid}, {'$set': {'done': 1}})
        number -= 1
        print(str(number) + '...left')

if __name__ == "__main__":
    while True:
        try:
            main_action()
        except Exception as e:
            print('error happens, after 10s the programme will continue...')
            sleep(10)