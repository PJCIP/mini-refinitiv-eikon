import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import companyinfo 
import pandas as pd


nlp = spacy.load('en_core_web_sm')

nlp.add_pipe("spacytextblob")


def data_preprocessing(text):
    
    all_stopwords = nlp.Defaults.stop_words
    # print(all_stopwords)
    punc_free = " ".join([token.orth_ for token in nlp(text) if not token.is_punct] )
    stop_free = " ".join([word for word in nlp(punc_free).text.split() if not word in all_stopwords])
    lemmatized = " ".join([word.lemma_ for word in nlp(stop_free)])
    

    return lemmatized

def sentiment_with_preprocess(text):

    filtered_text = data_preprocessing(text)
    print('preprocessed input')
    print(filtered_text)
    docx = nlp(filtered_text)
    sentiment_score = docx._.polarity
    assesment = docx._.assessments
    table = pd.DataFrame(assesment,columns=['Word','Polarity','Subjectivity','unkown'])
    return table,sentiment_score

def sentiment_without_preprocess(text):

    # filtered_text = data_preprocessing(text)
    # print(filtered_text)
    docx = nlp(text)
    sentiment_score = docx._.polarity
    assesment = docx._.assessments
    table = pd.DataFrame(assesment,columns=['Word','Polarity','Subjectivity','unkown'])
    return table,sentiment_score

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
    for entity in docx.ents:
        entities.append(entity.text+"("+spacy.explain(entity.label_)+")")
    # print(entities)    
    key_entity = ', '.join(list(set(entities)))
    return docx,sentiment_score,sub_words,text_summ,key_entity

symbol = 'aapl'
newsdata = companyinfo.fetch_news(symbol)
# text = newsdata[0]['summary']
# print(text)
text = '''We'll find the mistake mostly by end of this year.(Bloomberg) -- Apple Inc. would be prohibited under antitrust reform legislation introduced last week from giving its own apps an advantage by preventing users from removing them on Apple devices, said Democratic Representative David Cicilline, who is leading a push to pass new regulations for U.S. technology companies.Cicilline told reporters Wednesday that a proposal prohibiting tech platforms from giving an advantage to their own products over those of competitors would mean Apple must let co'''
docx,sentiment_score,sub_words,text_summ,key_entity = sentiment(text)
print(docx)
print(text_summ)
print(sub_words)
print(key_entity)
print(sentiment_score)

# print("preprocessing")
# processed = data_preprocessing(text)
# print("Before preprocessing {}after {}".format(len(text),len(processed)))
# print("Before preprocessing")
# table,ss = sentiment_without_preprocess(text)
# print(table)
# print(ss)
# print("After preprocessing")
# table,ss = sentiment_with_preprocess(text)
# print(table)
# print(ss)