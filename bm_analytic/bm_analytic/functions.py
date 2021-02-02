from numpy import nan
import pandas as pd
import dash  
import dash_table
import dash_core_components as dcc 
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.express as px
from gensim import models


#generate targetcomapny table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns],style={
            'max-width': '300px',
            'overflow': 'hidden',
            'text-overflow': 'ellipsis',
            'white-space': 'nowrap'
        })] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ],
        style={
            'max-width': '300px',
            'overflow': 'hidden',
            'text-overflow': 'ellipsis',
            'white-space': 'nowrap'
        }
        ) for i in range(min(len(dataframe), max_rows))]
    )

#########################################################
# 2021/2/2                                              #
# create pls × words similarities graph                 #
# x=pls, y = words vs companies fullocerview discription#
#########################################################
#make plot
def make_plot(df, word, x):
    tempdf = show_similar_companies(word, df, x)
    tempdf.columns = ['Name', 'overview', 'mainproducts', x, 'Similarity']
    return px.scatter(data_frame=tempdf, x=x, y='Similarity', hover_data=['Name'],title=word)
    # fig.show()

#similarities companies with full overview documentation
def show_similar_companies(word, df, x):
    results_df = pd.DataFrame()
    results_df = df.copy()
    results = get_similarities([word],list(df['Full_overview']))
    results = results.apply(abs)
    results_df['Similarity'] = results
    
    return results_df[['Company_Name', 'Full_overview', 'Primary_business_line', x, 'Similarity']]

#word vs lists similarities
def get_similarities(word, lists):
    #Import doc2vec model
    d2v = models.Doc2Vec.load('../bm_analytic/data/doc2vec.model')
    results = []
    for llist in lists:
        if type(llist) == str:
            (results.append(d2v.docvecs.similarity_unseen_docs(d2v, word, llist.split(' ')))) 
        else:
            results.append(nan)
    return pd.Series(results)