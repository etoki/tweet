from pprint import pprint
import spacy
import ginza

nlp = spacy.load('ja_ginza')
ginza.set_split_mode(nlp, 'C') # 分割単位C
doc = nlp('夏の全国高等学校野球選手権大会に出場する')

for token in doc:
    pprint(token)

