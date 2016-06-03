import scraperwiki
import lxml.html
import re

def name_reverse(name):
	reverse = name.split(',  ')
	reverse.reverse()
	return ' '.join(reverse)

def scraper_list(html):
	root = lxml.html.fromstring(html)
	for tr in root.cssselect('table.table tbody tr'):
		tds = tr.cssselect('td')
		id =  tds[0].cssselect("a")[0].get('href').split('/').pop()
		data = {
			'id': id,
			'image': 'http://www.senado.gov.ar'+tds[0].cssselect('img')[0].get('src'),
			'name':  name_reverse(re.sub(r'[\n\t]+', ' ', tds[1].text_content().strip())),
			'sort_name': re.sub(r'[\n\t]+', ' ', tds[1].text_content().strip()),
			'district':  re.sub(r'[\n\t]+', ' ', tds[2].text_content().strip()),
			'party':  re.sub(r'[\n\t]+', ' ', tds[3].text_content().strip()),
			'mandate_start':  tds[4].text_content().split("\n")[0].strip(),
			'mandate_end':  tds[4].text_content().split("\n")[1].strip(),
			'email':  tds[5].cssselect('a')[0].text_content().strip(),		
			'source': 'http://www.senado.gov.ar'+tds[0].cssselect("a")[0].get('href')
		}	
		data['phone'] = tds[5].text_content().split('\n')[2].strip() + ' ' + tds[5].text_content().split('\n')[4].strip()
		if len(tds[5].cssselect('a')) > 1: 
			link = tds[5].cssselect('a')[1].get('href').strip()
			if 'facebook' in link:
				data['facebook'] = tds[5].cssselect('a')[1].get('href').strip()
			else: 
				data['twitter'] = tds[5].cssselect('a')[1].get('href').strip()
		if len(tds[5].cssselect('a')) > 2: 
			data['twitter'] = tds[5].cssselect('a')[2].get('href').strip()
		
		#print data
		scraperwiki.sqlite.save(unique_keys=['id'], data=data)


scraper_list(scraperwiki.scrape('http://www.senado.gov.ar/senadores/listados/listaSenadoRes'))