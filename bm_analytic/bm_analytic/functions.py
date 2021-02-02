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
# filter functions                                      #
#                                                       #
#########################################################
#filter function
def fil_func(col_nm,val,df):
    if  val is None or val == '' or not val:
        pass
    else:
        df = df[df[col_nm].isin(val)]
    return df
#filter function with R&D/sales = Research_&_Development_expenses ÷ Operating_Revenue_/_Turnover
def fil_RDsales_func(RDsalesVal,CoveredYearVal,YearSpan,df):
    if RDsalesVal is None or RDsalesVal == '' or not RDsalesVal or 0:
        pass
    else:
        df = df.assign(RDsales_total=0)
        for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
            df['RDsales_total'] = df['RDsales_total'] + (df['Research_&_Development_expenses_th_LCU_' + str(i)] / df['Operating_Revenue_/_Turnover_th_LCU_' + str(i)])
        df['RD/sales'] = df['RDsales_total']/(YearSpan)
        # filter
        df = df[df['RD/sales'] <= RDsalesVal/100]
    return  df
#filter function with SGA/sales = SGA ÷ Operating_Revenue_/_Turnover
def fil_SGAsales_func(SGAsalesVal,CoveredYearVal,YearSpan,df):
    if SGAsalesVal is None or SGAsalesVal == '' or not SGAsalesVal or 0:
        pass
    else:
        df = df.assign(SGAsales_total=0)
        for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
            df['SGAsales_total'] = df['SGAsales_total'] + (df['SGA_' + str(i)] / df['Operating_Revenue_/_Turnover_th_LCU_' + str(i)])
        df['SGA/sales'] = df['SGAsales_total']/(YearSpan)
        # filter
        df = df[df['SGA/sales'] <= SGAsalesVal/100]
    return df

#########################################################
# 2021/2/2                                              #
# Create PLI data with coverd year                      #
#                                                       #
#########################################################
def create_PLI_data(CoveredYearVal,YearSpan,df):
    #PLI OM = Operating Profit ÷ Operating Revenue 
    df['OM_total'] = 0
    for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
        df['OM_total'] = df['OM_total'] + df['Operating Profits Margin_' + str(i)]
    df['OM'] = df['OM_total']/(YearSpan)
    #PLI TCM = Operating P/L ÷ (Operating Revenue - Operating P/L)
    df['TCM_total'] = 0
    for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
        df['TCM_total'] = df['TCM_total'] + df['Total Cost-Markup_' + str(i)]
    df['TCM'] = df['TCM_total']/(YearSpan)
    #Berry Ratio = Gross Profit ÷ Selling, General & Administrative Expenses
    df['BerryRatio_total'] = 0
    for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
        df['BerryRatio_total'] = df['BerryRatio_total'] + df['Berry Ratio_' + str(i)]
    df['BerryRatio'] = df['BerryRatio_total']/(YearSpan)
    return df

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