from numpy import nan
import pandas as pd

# Import Comanies Data
df = pd.read_csv('../bm_analytic/data/BM_DataSet_1000.csv', index_col=0)

# Create Senteces
sentences = []
for text in df['Full_overview'].astype(str):
    text_list = text.split(' ')
    sentences.append(text_list)

# Modeling
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(sentences)]
########################################################################################################################
# https://radimrehurek.com/gensim/models/doc2vec.html
# epochs (int, optional) – Number of iterations (epochs) over the corpus. Defaults to 10 for Doc2Vec.
# vector_size (int, optional) – Dimensionality of the feature vectors.
# window (int, optional) – The maximum distance between the current and predicted word within a sentence.
# min_count (int, optional) – Ignores all words with total frequency lower than this.
# workers (int, optional) – Use these many worker threads to train the model (=faster training with multicore machines).
########################################################################################################################
model = Doc2Vec(documents, epoch=20, vector_size=50, window=15, min_count=2, workers=4)
model.save('doc2vec.model')