import requests
from bs4 import BeautifulSoup
import time
from Publication import *
baseURL = 'https://scholar.google.com'


headers = {'authority':'scholar.google.com',
'method': 'GET',
'path': '/citations?hl=en&user=k-iFVJAAAAAJ&view_op=list_works&alert_preview_top_rm=2&sortby=pubdate',
'scheme': 'https',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'cache-control': 'max-age=0',
'cookie':'CONSENT=YES+US.en+; GSP=LM=1628806446:S=0UAGihFshELXYd2D; HSID=AV7RAe5RHKeFlqhJF; SSID=AQ2KxhLXTdBYWfMlh; APISID=35qkOKQhwGu4rZxy/A-K9NG-wqSMe3KPy0; SAPISID=ya_c9-6dOHgIBArN/AJo1razcK9X1bV6Iy; __Secure-1PAPISID=ya_c9-6dOHgIBArN/AJo1razcK9X1bV6Iy; __Secure-3PAPISID=ya_c9-6dOHgIBArN/AJo1razcK9X1bV6Iy; SEARCH_SAMESITE=CgQI_pMB; __Secure-1PSIDCC=AJi4QfEUCebtHc0q3qUomSzqnuKn0q9vbADAPtEPUdSAJNUXWdsV1qbMl9jXdjvHwnMfz_aU7A; SID=EgiT6EV7sxjvU3a1QokcV3uVsBPYTKtWTo70D2J9VzscRp3kZAy7IEWs7pJ5-5BVJiMyRg.; __Secure-1PSID=EgiT6EV7sxjvU3a1QokcV3uVsBPYTKtWTo70D2J9VzscRp3kjNLZ3yPTHmYKesvRiurMrA.; __Secure-3PSID=EgiT6EV7sxjvU3a1QokcV3uVsBPYTKtWTo70D2J9VzscRp3khi487ikdsDZwnbcOoeU-AQ.; OGPC=19022519-1:19022622-1:; NID=511=tqssQqcY_1SJhJRH8ffTnsjCnJvAA7bYXy18J55o1puq0-lYRGTxHZA2wTvMN7MRJqaZSk1ILkLn6zoJCGP4XxIilmVtYq4EQ7Dt2AGy_auZ_eOfKl1SOaG0K8Ko6CTV7md93l1kongDdTyYMnfthqXfdEonaRH_qGYPdgig03TskxG8pu_xRgL-7Zku9T3EB9Lj6YsBzsSB0gK5FCKG6yrQhEgcuYEoUJYRyhXCWQz9cuvOjyg2ik-xR03OQ0p_ZLloPSgCOQh-CeYIdkj_35S6; 1P_JAR=2021-12-30-16; SIDCC=AJi4QfFCYrqTPoPBy_mxOYg9YWNo6mZkJADyn1pDvSmPEPtuXTizUpMlzJO4k-JFAez3e9ghKW36; __Secure-3PSIDCC=AJi4QfEa0jGZvicG3cMWrA8gdUDnAvwED8hVU11aGyLZBNGfzrD9u1q5Dierpr1gOb0mSUtuVT8b',
'referer': 'https://scholar.google.com/citations?user=k-iFVJAAAAAJ&hl=en',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': "Windows",
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'x-client-data': 'CI62yQEIprbJAQjEtskBCKmdygEIwf3KAQjq8ssBCJ75ywEI1vzLAQjmhMwBCLaFzAEIy4nMAQitjswBCNKPzAEI2pDMARirqcoBGI6eywEYh47MAQ=='
}
mainPageURL = 'https://scholar.google.com/citations?hl=en&user=k-iFVJAAAAAJ&view_op=list_works&alert_preview_top_rm=2&sortby=pubdate'
#mainPageURL = 'https://scholar.google.com/citations?hl=en&user=sXhCz3YAAAAJ&view_op=list_works&alert_preview_top_rm=2&sortby=pubdate'
html_main = requests.get(mainPageURL,headers=headers).text
mainPage = BeautifulSoup(html_main,'lxml')
articles = mainPage.find_all('tr',class_='gsc_a_tr')

with open('pubs.bib', 'w') as bibF:
	bibF.write('')

with open('pubs.txt', 'w') as txtF:
	txtF.write('')
	
for article in articles:
	print('sleeping')
	time.sleep(2)#need to sleep to prevent google from getting mad at fast requests
	print()
	info = article.find('a')
	detailsPageURL = baseURL + info.attrs['href']
	print(f'article found: {info.contents[0]}')
	html_details = requests.get(detailsPageURL,headers=headers).text
	detailsPage = BeautifulSoup(html_details,'lxml')
	detailsTable = detailsPage.find_all('div',id='gsc_oci_table')[0]
	pub = Publication(title=info.contents[0])
	pub.url = detailsPageURL
	for det in detailsTable.contents:
		fieldType =det.find('div',class_='gsc_oci_field').text.lower().replace(' ','')
		if fieldType in pub.pub_attrs:
				setattr(pub,fieldType,det.find('div',class_='gsc_oci_value').text)
	print(pub)
	with open('pubs.bib', 'a+') as bibF:
		bibF.write(pub.printBibEntry('JAB:'))
		bibF.write('\n\n')
	with open('pubs.txt', 'a+') as txtF:
		txtF.write(pub.printPlain())
		txtF.write('\n\n')

