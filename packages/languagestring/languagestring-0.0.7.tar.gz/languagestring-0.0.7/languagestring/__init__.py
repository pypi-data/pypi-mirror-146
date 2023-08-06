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
			return ''.join(self.language_dict[language]['lowercase']['letter'])
		elif case == 'uppercase':
			return ''.join(self.language_dict[language]['uppercase']['letter'])
		elif case == 'other':
			return ''.join(self.language_dict[language]['other']['letter'])
		else:
			return ''.join(self.language_dict[language]['lowercase']['letter']) + ''.join(self.language_dict[language]['uppercase']['letter']) + ''.join(self.language_dict[language]['other']['letter'])

	def language_array(self,language,case='all'):
		if case == 'lowercase':
			return self.language_dict[language]['lowercase']['letter']
		elif case == 'uppercase':
			return self.language_dict[language]['uppercase']['letter']
		elif case == 'other':
			return self.language_dict[language]['other']['letter']
		else:
			return self.language_dict[language]['lowercase']['letter'] + self.language_dict[language]['uppercase']['letter'] + self.language_dict[language]['other']['letter']
	
	def alt_codes(self,language,case='all'):
		if case == 'lowercase':
			return self.language_dict[language]['lowercase']['alt_code']
		elif case == 'uppercase':
			return self.language_dict[language]['uppercase']['alt_code']
		elif case == 'other':
			return self.language_dict[language]['other']['alt_code']
		else:
			return self.language_dict[language]['lowercase']['alt_code'] + self.language_dict[language]['uppercase']['alt_code'] + self.language_dict[language]['other']['alt_code']

	
	def description(self,language,case='all'):
		if case == 'lowercase':
			return self.language_dict[language]['lowercase']['description']
		elif case == 'uppercase':
			return self.language_dict[language]['uppercase']['description']
		elif case == 'other':
			return self.language_dict[language]['other']['description']
		else:
			return self.language_dict[language]['lowercase']['description'] + self.language_dict[language]['uppercase']['description'] + self.language_dict[language]['other']['description']



if __name__ == "__main__":
	ls = languagestring()
	print(ls.string.ascii_lowercase)
	print(ls.description('cz',case='all'))
