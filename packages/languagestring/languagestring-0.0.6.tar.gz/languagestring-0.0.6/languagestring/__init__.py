import string, json,os

class languagestring(object):
	def __init__(self):
		self.string = string
		cp ='/'.join( f'{os.path.realpath(__file__)}'.split('/')[:-2])
		with open(f'{cp}/languagestring/assets/language_detailed.json','r') as f:
			self.language_dict = json.load(f)
			f.close()


	def language_string(self,language,case='all'):
		if case == 'lowercase':
			return ''.join(ls.language_dict[language]['lowercase']['letter'])
		elif case == 'uppercase':
			return ''.join(ls.language_dict[language]['uppercase']['letter'])
		elif case == 'other':
			return ''.join(ls.language_dict[language]['other']['letter'])
		else:
			return ''.join(ls.language_dict[language]['lowercase']['letter']) + ''.join(ls.language_dict[language]['uppercase']['letter']) + ''.join(ls.language_dict[language]['other']['letter'])

	def language_array(self,language,case='all'):
		if case == 'lowercase':
			return ls.language_dict[language]['lowercase']['letter']
		elif case == 'uppercase':
			return ls.language_dict[language]['uppercase']['letter']
		elif case == 'other':
			return ls.language_dict[language]['other']['letter']
		else:
			return ls.language_dict[language]['lowercase']['letter'] + ls.language_dict[language]['uppercase']['letter'] + ls.language_dict[language]['other']['letter']
	
	def alt_codes(self,language,case='all'):
		if case == 'lowercase':
			return ls.language_dict[language]['lowercase']['alt_code']
		elif case == 'uppercase':
			return ls.language_dict[language]['uppercase']['alt_code']
		elif case == 'other':
			return ls.language_dict[language]['other']['alt_code']
		else:
			return ls.language_dict[language]['lowercase']['alt_code'] + ls.language_dict[language]['uppercase']['alt_code'] + ls.language_dict[language]['other']['alt_code']

	
	def description(self,language,case='all'):
		if case == 'lowercase':
			return ls.language_dict[language]['lowercase']['description']
		elif case == 'uppercase':
			return ls.language_dict[language]['uppercase']['description']
		elif case == 'other':
			return ls.language_dict[language]['other']['description']
		else:
			return ls.language_dict[language]['lowercase']['description'] + ls.language_dict[language]['uppercase']['description'] + ls.language_dict[language]['other']['description']



if __name__ == "__main__":
	ls = languagestring()
	print(ls.string.ascii_lowercase)
	print(ls.description('cz',case='all'))
