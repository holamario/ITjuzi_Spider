import urllib.request as fetch
from investmentevent import investmentevent
import re
'''url='https://www.itjuzi.com/investevents/16271'

response=fetch.urlopen(url)
response=response.read().decode('utf8')

print(response)'''
#print(investmentevent(1151))
url='https://www.itjuzi.com/investevents?page=1151'
resp=fetch.urlopen(url)
response=resp.read().decode('utf8')
print(resp)

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
    print(r1)
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