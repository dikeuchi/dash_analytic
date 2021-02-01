from numpy import nan
import pandas as pd



#Import Comanies Data
df = pd.read_csv('../bm_analytic/data/BM_DataSet_1000.csv', index_col=0)

sentences = []
for text in df['Primary_business_line'].astype(str):
    text_list = text.split(' ')
    sentences.append(text_list)

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(sentences)]
model = Doc2Vec(documents, vector_size=2, window=5, min_count=1, workers=4)
model.save('doc2vec.model')