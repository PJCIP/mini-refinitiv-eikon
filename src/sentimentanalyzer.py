import spacy
from spacytextblob.spacytextblob import SpacyTextBlob 
import pandas as pd

nlp = spacy.load('en_core_web_sm')

nlp.add_pipe("spacytextblob")



def sentiment(text):
    entities = []
    docx = nlp(text)
    sentiment_score = docx._.polarity
    assesment = docx._.assessments
    table = pd.DataFrame(assesment,columns=['Word','Polarity','Subjectivity','unkown'])
    sub_words = list(map(lambda x: x[0],table['Word']))
    for words in sub_words:
         text = text.replace(words,"** {} **".format(words))
    text_summ = text     
    sub_words = ', '.join(sub_words)
    for entity in docx.ents:
        entities.append(entity.text+"("+entity.label_+")")
    # print(entities)    
    key_entity = ', '.join(entities)
    return docx,sentiment_score,sub_words,text_summ,key_entity
# text = '''Apple, Microsoft and Google are in bases, but which is the most promising? To be a big stock market winner, be a small loser.'''
# sentiment(text)

