from dataclasses import dataclass,field
@dataclass
class Publication():
	
	authors:list[str]=field(default_factory=list)
	title:str=''
	journal:str=''
	publisher:str=''
	conference:str=''
	pages:str=''
	citations:str=''
	publicationdate:str=''
	url:str=''
	def __post_init__(self):
		self.pub_attrs =['authors','title','journal','conference','pages','publisher','publicationdate','citations','url']

	def __repr__(self):
		outStr = f"{self.title}\n"
		outStr+= f"{self.authors}\n"
		outStr+= f"{self.conference if self.journal == '' else self.journal}\n"
		outStr+= f"{self.publisher}\n"
		outStr+= f"citations: {self.citations}\n"
		outStr+= f"{self.url}\n"
		return outStr
	def __str__(self):
		return self.__repr__()
	def printPlain(self):
		outStr = ''
		dateList = self.publicationdate.split('/')
		year = ''
		for d in dateList:
			if len(d) == 4:
				year = d
		authors = ' and '.join(self.authors.split(','))
		outStr += self.title + '\n'
		outStr += authors + '\n'
		outStr += self.conference if self.journal == '' else self.journal
		outStr += ', '
		outStr += self.publicationdate + ', '
		outStr += self.url
		return outStr


	def printBibEntry(self,key=''):
		dateList = self.publicationdate.split('/')
		year = ''
		for d in dateList:
			if len(d) == 4:
				year = d
		authors = ' and '.join(self.authors.split(','))
		firstAuthor_lastName = self.authors.split(',')[0].split(' ')[-1]
		key = key+firstAuthor_lastName[0:3] + year
		authors = ' and '.join(self.authors.split(','))
		if self.journal == '':
			bibString = f'@inproceedings{"{"}{key},\n author="{authors}",\n booktitle="{self.conference}",\npublisher="{self.publisher}",\n title="{self.title}",\n year="{year}",\npages="{self.pages},"{"}"}'
		else:
			bibString = f'@article{"{"}{key},\n author="{authors}",\n journal="{self.journal}",\n publisher="{self.publisher}",\n title="{self.title}",\n year="{year}",\n pages="{self.pages}"{"}"}'
		return bibString
		


		
