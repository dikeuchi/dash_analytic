from numpy import nan
import pandas as pd

# Import Comanies Data
df = pd.read_csv('../bm_analytic/data/BM_DataSet_1000.csv', index_col=0)

# Create Senteces
sentences = []
for text in df['Full_overview'].astype(str):
    text_list = text.split(' ')
    sentences.append(text_list)

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(sentences)]
model = Doc2Vec(documents, epoch=20, vector_size=50, window=15, min_count=2, workers=4)
model.save('doc2vec.model')