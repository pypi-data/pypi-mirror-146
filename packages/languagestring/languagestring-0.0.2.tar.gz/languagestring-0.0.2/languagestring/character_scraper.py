import requests,json, os
from bs4 import BeautifulSoup


def scraper():
	with open(f'{os.path.realpath(__file__)}/languagestring/assets/mapping.json','r') as f:
		languages = json.load(f)
		f.close()
	print(languages) 
	language_dict = {}
	for language in list(languages.keys()):
		print(language)
		language_dict[language] = {}
		language_dict[language]['lowercase'] = {'letter':[],'alt_code':[],'description':[]}
		language_dict[language]['uppercase'] = {'letter':[],'alt_code':[],'description':[]}
		language_dict[language]['other'] = {'letter':[],'alt_code':[],'description':[]}
		r = requests.get(f'https://altcodeunicode.com/alt-codes-for-{languages[language]}-letters-with-accents-or-diacritics/')
		soup = BeautifulSoup(r.text,features="lxml")
		tables = soup.select('table')
		print(tables)
		print(len(tables))
		table = tables[0]
		trs = table.select('tr')
		print(trs)
		i = 0
		for tr in trs:

		
			j = 0
			if i == 0:
				i += 1
				continue
			tds = tr.select('td')
			for td in tds:
				print(td)
				if j == 0 :
					current_letter = td.text.strip()
				elif j == 1:
					current_alt_code = td.text.strip()
				elif j == 2:
					current_description = td.text.strip()
				
				j += 1

				#raise 'ee'
			print(current_letter,current_alt_code,current_description)
			if 'small letter' in current_description:
				letters = language_dict[language]['lowercase']['letter']
				alt_code = language_dict[language]['lowercase']['alt_code']
				descriptions = language_dict[language]['lowercase']['description']
			elif 'capital letter' in current_description:
				letters = language_dict[language]['uppercase']['letter']
				alt_code = language_dict[language]['uppercase']['alt_code']
				descriptions = language_dict[language]['uppercase']['description']				
			else:
				letters = language_dict[language]['other']['letter']
				alt_code = language_dict[language]['other']['alt_code']
				descriptions = language_dict[language]['other']['description']					

			letters.append(current_letter)
			alt_code.append(current_alt_code)
			descriptions.append(current_description)
			if 'small letter' in current_description:
				language_dict[language]['lowercase']['letter'] = letters
				language_dict[language]['lowercase']['alt_code'] = alt_code
				language_dict[language]['lowercase']['description'] = descriptions
			elif 'capital letter' in current_description:
				language_dict[language]['uppercase']['letter'] = letters
				language_dict[language]['uppercase']['alt_code'] = alt_code
				language_dict[language]['uppercase']['description']	= descriptions
			else:
				language_dict[language]['other']['letter'] = letters
				language_dict[language]['other']['alt_code'] = alt_code
				language_dict[language]['other']['description']	= descriptions			
		#raise 'ee'
		print(language_dict)
	with open(f'{os.path.realpath(__file__)}/languagestring/assets/language_detailed.json','w') as f:
		json.dump(language_dict,f)
		f.close()

if __name__ == "__main__":
	ss = scraper()#["se","fr","de","nl","es","pt","pl","cz","it"])


"""					letters = language_dict[language]['lowercase']['letter']
					current_letter = td.text
					letters.append(current_letter)
					language_dict[language]['lowercase']['letter'] = letters	"""