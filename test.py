import urllib.request as fetch
import re

url = 'https://www.itjuzi.com/investevents?pageview=1'
response = fetch.urlopen(url)
response = response.read().decode('utf8')

pattern = re.compile('<ul class="list-main-eventset">(.*?)</ul>', re.S)
results = re.findall(pattern, response)
results = results[0].replace('\t', '').replace('\n', '')
pattern2 = re.compile('<li>(.*?)</li>')
results2 = re.findall(pattern2, results)
print(results2)
# print(response)
t = '<i class="cell round"><span>2016.4.14</span></i><i class="cell pic"><a target="_blank" href="https://www.itjuzi.com/investevents/16255"><span class="incicon"><img src="https://www.itjuzi.com/images/47afcb101339c8a824de3ef23f4ee6ca.jpg"></span></a></i><i class="cell maincell"><p class="title"><a target="_blank" href="https://www.itjuzi.com/investevents/16255"><span>哈视奇</span></a></p><p><span class="tags t-small c-gray-aset"><a href="https://www.itjuzi.com/investevents?scope=80">游戏</a></span><span class="loca c-gray-aset t-small"><a href="https://www.itjuzi.com/investevents?prov=北京">北京</a></span></p></i><i class="cell round"><a><span class="tag gray">天使轮</span></a></i><i class="cell fina">数百万人民币</i><i class="cell date"><span class="investorset"><a target="_blank" href="https://www.itjuzi.com/investfirm/21">清科创投</a><br><a target="_blank" href="https://www.itjuzi.com/investfirm/2442">集素资本</a><br><span class="c-gray">鼎视传媒</span><br/></span></i>'
