import urllib.request as fetch

url='https://www.itjuzi.com/investevents/16271'

response=fetch.urlopen(url)
response=response.read().decode('utf8')

print(response)