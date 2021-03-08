import requests

from bs4 import BeautifulSoup

modern_poets = ['james-tate', 'billy-collins', 'john-ashbery', 'charles-simic']

romantic_poets = ['john-keats', 'george-gordon-byron-3', 'william-wordsworth', 'william-blake']

renaissance_poets = ['john-donne', 'william-shakespeare', 'john-milton', 'sir-thomas-wyatt']

poets_dict = {}

poets = modern_poets

for poet in poets: 
        
    URL = 'https://www.poemhunter.com/' + poet + '/poems/'
    
    URL2 = URL + 'page-2/'
    
    URL3 = URL + 'page-3/'
    
    urls = [URL, URL2, URL3]
    
    poet_corpus = ""
        
    for url in urls:
        
        page = requests.get(url)
        
        soup = BeautifulSoup(page.content, 'html.parser')
        
        results = soup.find(id="profilePoems")
        
        #print(results.prettify())
        
        x = results.find_all('div', class_='phlText')
        
        import re
        
        y = re.findall("\/[poem/].*/\"", str(x))
        
        for page in y:
            URL = 'https://www.poemhunter.com/' + page[1:-1]
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find("script",type="application/ld+json")
            #print(results.prettify())
            mess = re.findall('["genre": "poetry",\r\n                "inLanguage": "en",\r\n               ].*[\r\n                },\r\n                    {\r\n        "@id": "https://www.poemhunter.com",\r\n        "@type": "Organization",\r\n        "address":]', results.text)
            mess = mess[24].replace('\r', '\n')
            #print(mess[25:-3])
            poet_corpus += mess[25:-3]

    poets_dict[poet] = poet_corpus



import nltk, re, random
from nltk.tokenize import word_tokenize
from collections import defaultdict, deque

class MarkovChain:
    def __init__(self, mylen):
      self.mylen = mylen
      self.lookup_dict = defaultdict(list)
      self._seeded = False
      self.__seed_me()
               
    def __seed_me(self, rand_seed=None):
      if self._seeded is not True:
        try:
          if rand_seed is not None:
            random.seed(rand_seed)
          else:
            random.seed()
          self._seeded = True
        except NotImplementedError:
          self._seeded = False
      
    def add_document(self, str):
      preprocessed_list = self._preprocess(str)
      pairs = self.__generate_tuple_keys(preprocessed_list)
      for pair in pairs:
        self.lookup_dict[pair[0]].append(pair[1])
    
    def _preprocess(self, str):
      cleaned = re.sub(r'\W+', ' ', str).lower()
      tokenized = word_tokenize(cleaned)
      return tokenized
    
    def __generate_tuple_keys(self, data):
      if len(data) < 1:
        return
    
      for i in range(len(data) - 1):
        yield [ data[i], data[i + 1] ]
        
    def generate_text(self):
      context = deque()
      output = []
      if len(self.lookup_dict) > 0:
        self.__seed_me(rand_seed=len(self.lookup_dict))
        chain_head = [list(self.lookup_dict)[0]]
        context.extend(chain_head)
        
        while len(output) < (self.mylen - 1):
          next_choices = self.lookup_dict[context[-1]]
          if len(next_choices) > 0:
            next_word = random.choice(next_choices)
            context.append(next_word)
            output.append(context.popleft())
          else:
            break
        output.extend(list(context))
      return " ".join(output)



my_markov = MarkovChain(mylen=140)

for poet in poets:
    my_markov.add_document(poets_dict[poet])

generated_text = my_markov.generate_text()
print(generated_text)


f = open("MyNewPoem.txt", "w")
f.write(generated_text)
f.close()
