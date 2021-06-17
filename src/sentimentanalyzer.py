import spacy
from spacytextblob.spacytextblob import SpacyTextBlob 
import pandas as pd

nlp = spacy.load('en_core_web_sm')

nlp.add_pipe("spacytextblob")

def data_preprocessing(text):
    
    all_stopwords = nlp.Defaults.stop_words
    punc_free = " ".join([token.orth_ for token in nlp(text) if not token.is_punct] )
    stop_free = " ".join([word for word in nlp(punc_free).text.split() if not word in all_stopwords])
    lemmatized = " ".join([word.lemma_ for word in nlp(stop_free)])
    

    return lemmatized

def sentiment(text):
    entities = []
    tablewords = []
    filtered_text = data_preprocessing(text)
    docx = nlp(filtered_text)
    sentiment_score = docx._.polarity
    assesment = docx._.assessments
    table = pd.DataFrame(assesment,columns=['Word','Polarity','Subjectivity','unkown'])
    sub_words = list(map(lambda x: x[0],table['Word']))
    sub_words_processed = list(set(sub_words))
    for words in sub_words_processed:
         text = text.replace(words,"** {} **".format(words))
    text_summ = text     
    sub_words = ', '.join(sub_words)
    for entity in nlp(text).ents:
        entities.append(entity.text+"("+spacy.explain(entity.label_)+")")
    key_entity = ', '.join(list(set(entities)))
    return docx,sentiment_score,sub_words,text_summ,key_entity


