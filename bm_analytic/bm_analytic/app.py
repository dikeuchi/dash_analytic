from numpy import nan
import pandas as pd
import dash  
import dash_core_components as dcc 
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.express as px
from gensim import models

#Import Comanies Data
df_basic = pd.read_csv('../bm_analytic/data/BM_DataSet_1000.csv', index_col=0)
# df_basic = pd.read_csv('../data/BM_DataSet.csv', index_col=0)
#Import doc2vec model
d2v = models.Doc2Vec.load('../bm_analytic/data/doc2vec.model')

#filter後
fil_df = df_basic.copy()

#master情報のみ
df_master = df_basic.drop(columns=['Operating Profits Margin_2018','Operating Profits Margin_2017','Operating Profits Margin_2016','Operating Profits Margin_2015','Operating Profits Margin_2014','Operating Profits Margin_2013','Operating Profits Margin_2012','Operating Profits Margin_2011','Operating Profits Margin_2010','Total Cost-Markup_2018','Total Cost-Markup_2017','Total Cost-Markup_2016','Total Cost-Markup_2015','Total Cost-Markup_2014','Total Cost-Markup_2013','Total Cost-Markup_2012','Total Cost-Markup_2011','Total Cost-Markup_2010','SGA_2018','SGA_2017','SGA_2016','SGA_2015','SGA_2014','SGA_2013','SGA_2012','SGA_2011','SGA_2010','Berry Ratio_2018','Berry Ratio_2017','Berry Ratio_2016','Berry Ratio_2015','Berry Ratio_2014','Berry Ratio_2013','Berry Ratio_2012','Berry Ratio_2011','Berry Ratio_2010'])

#sort用
indep = df_master['Indep'].unique()
indep.sort()
country = df_master['Country'].unique()
country.sort()
ussic = df_master['US_SIC_Primary_code(s)_(M)'].unique()
ussic.sort()
#functionの抽出
mainactivity = df_master['Main_activity'].str.split('; ', expand=True)
mainactivity = mainactivity.iloc[1]


#word vs lists similarities
def get_similarities(word, lists):
    results = []
    for llist in lists:
        if type(llist) == str:
            (results.append(d2v.docvecs.similarity_unseen_docs(d2v, word, llist.split(' ')))) 
        else:
            results.append(nan)
    return pd.Series(results)

#similarities companies
def show_similar_companies(word, df, x='Operating Profits Margin_2018'):
    results_df = pd.DataFrame()
    results_df = df.copy()
    results = get_similarities([word],list(df_basic['Primary_business_line']))
    results = results.apply(abs)
    results_df['Similarity'] = results
    
    return results_df[['Company_Name', 'Full_overview', 'Primary_business_line', x, 'Similarity']]

#make plot
def make_plot(df, word, x):
    tempdf = show_similar_companies(word, df, x)
    tempdf.columns = ['Name', 'overview', 'mainproducts', x, 'Similarity']
    return px.scatter(data_frame=tempdf, x=x, y='Similarity', hover_data=['Name'],title=word)
    # fig.show()

#表の作成
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(id='my-div',children=[
    #title
    html.H4(children='BM Analytics'),
    #target Div
    html.Div(id='Target',children=[
        #target select
        html.Div(id='targetserch',children=[
        #Target Company
        html.P('Target Company'),
        dcc.Dropdown(
            id = 'dropdown-target',
            options = [{'label': i, 'value': i} for i in df_master['Company_Name'].unique()],
            value = '',
            style={'padding':'5px','height':'10%'}
        )
        ], style={
            'width': 'calc(100% *1.5/ 5)',
            'border-radius': '5px',
            'background-color': '#f9f9f9',
            'margin': '10px',
            'padding': '15px',
            'position': 'relative',
            'box-shadow': '2px 2px 2px lightgrey'
            }
        ),

        #target info
        html.Div(id='targetcompany',children=[
            #Target Company
             html.P('Target Company Info'),
            #company table
                html.Div(id='companyinfo',children=[
                    
                ], style={
                    'float': 'bottom',
                    'display': 'block',
                    'overflow-x': 'scroll',
                    'border-radius': '5px',
                    'background-color': '#f9f9f9',
                    'margin': '10px',
                    'padding': '15px',
                    'position': 'relative',
                    'box-shadow': '2px 2px 2px lightgrey'
                })
        ], style={
            'width': 'calc(100% *3.5/ 5)',
            'border-radius': '5px',
            'background-color': '#f9f9f9',
            'margin': '10px',
            'padding': '15px',
            'position': 'relative',
            'box-shadow': '2px 2px 2px lightgrey'
            }
        )
    ],style={
        'display':'flex'}
    ),

    #flexのfield
    html.Div(id='serchfield',children=[
        #検索条件
        html.Div(id='filter', children=[

            #Covered year
            html.P('Covered Year:',className='fil',style={'padding':'5px','width': '30%'}),
            html.Div(id='CoveredYear', children=[
                dcc.RangeSlider(
                    id='CoveredYearVal',
                    className='fil',
                    min=2010,
                    max=2018,
                    step=None,
                    marks={
                        2010:'2010',
                        2011:'2011',
                        2012:'2012',
                        2013:'2013',
                        2014:'2014',
                        2015:'2015',
                        2016:'2016',
                        2017:'2017',
                        2018:'2018'
                    },
                    value=[2016,2018]
                )
            ],style={'width':'90%','height':'10%'}),


            #checkbox:企業活動
            html.Div(id='Status', children=[
                html.P('Status Active:' ,className='fil',style={'padding':'5px','width': '30%'}),
                dcc.Checklist(
                    id='StatusVal',
                    className='fil',
                    options=[
                        {'label': '', 'value': 'Active'}
                    ],
                    value=['Active'],
                    style={'padding':'5px'}
                )
            ],style={'display':'flex','width':'100%','height':'10%'}),
            

            #独立性
            html.Div(id='Indep', children=[
                html.P('Indep:' ,className='fil',style={'padding':'5px','width': '30%'}),
                dcc.Dropdown(
                    id='IndepVal',
                    className='fil',
                    options=[{'label': i, 'value': i} for i in indep],
                    multi=True,
                    value='',
                    style={'padding':'5px','width':'100%'}
                ),
            ],style={'display':'flex'}),

            #所在国
            html.Div(id='Country', children=[
                html.P('Country:' ,className='fil',style={'padding':'5px','width': '30%'}),
                dcc.Dropdown(
                    id='CountryVal',
                    className='fil',
                    options=[{'label': i, 'value': i} for i in country],
                    multi=True,
                    value='',
                    style={'padding':'5px','width':'100%'}
                )
            ],style={'display':'flex'}),

            #US SIC
            html.Div(id='USSIC', children=[
                html.P('US SIC:' ,className='fil',style={'padding':'5px','width': '30%'}),
                dcc.Dropdown(
                    id='USSICVal',
                    className='fil',
                    options=[{'label': i, 'value': i} for i in ussic],
                    multi=True,
                    value='',
                    style={'padding':'5px','width':'100%'}
                )
            ],style={'display':'flex'}),

            #Available Years
            html.Div(id='AvailableYears', children=[
                html.P('Available Years:' ,className='fil',style={'padding':'5px','width': '30%'}),
                dcc.Dropdown(
                    id='AvailableYearsVal',
                    className='fil',
                    options=[{'label': 1, 'value': 1},{'label': 2, 'value': 2},{'label': 3, 'value': 3},{'label': 4, 'value': 4}],
                    value='',
                    style={'padding':'5px','width':'100%'}
                )
            ],style={'display':'flex','height':'10%'}),

            #checkbox:3-yr Loss
            html.Div(id='3yrLoss', children=[
                html.P('3-yr Loss:' ,className='fil',style={'padding':'5px','width': '30%'}),
                dcc.Checklist(
                    id='3yrLossVal',
                    className='fil',
                    options=[
                        {'label': '','value': 1}
                    ],
                    value=[1],
                    style={'padding':'5px'}
                )
            ],style={'display':'flex','width':'100%','height':'10%'}),

           #Product Input
           html.Div(id='Product', children=[
                html.P('Product:' ,className='fil',style={'padding':'5px','width': '30%'}),
                dcc.Input(id='ProductVal', type='text', value='', style={'width':'100%','padding':'5px'})
            ],style={'display':'flex','width':'100%','height':'10%'})

        ], style={
            'width': 'calc(100% *1/ 5)',
            'height':'80vh',
            'border-radius': '5px',
            'background-color': '#f9f9f9',
            'margin': '10px',
            'padding': '15px',
            'position': 'relative',
            'box-shadow': '2px 2px 2px lightgrey'
            }
        ),


        #dynamicFilter
        html.Div(id='dynamicFilter',children=[

            #Function
            html.P('Main Activity:' ,className='dynamic',style={'padding':'5px'}),
            dcc.Dropdown(
                id='MainactivityVal',
                className='dynamic',
                options=[{'label': i, 'value': i} for i in mainactivity],
                multi=True,
                value='',
                style={'padding':'5px','width':'100%'}
            ),


            #R&D/sales
            html.P('R&D/sales:' ,className='dynamic',style={'padding':'5px','padding-top': '50px'}),
            html.Div(id='R&Dsales',children=[
                daq.Slider(
                    id='R&DsalesVal',
                    min=0,
                    max=10,
                    value=0,
                    handleLabel={'showCurrentValue': True,'label': '%'},
                    step=0.1
                )
            ], style={
                'padding-top': '35px'
            }
            ),

            #SGA/sales
            html.P('SGA/sales:' ,className='dynamic',style={'padding':'5px','padding-top': '50px'}),
            html.Div(id='SGAsales',children=[
                daq.Slider(
                    id='SGAsalesVal',
                    min=0,
                    max=100,
                    value=50,
                    handleLabel={'showCurrentValue': True,'label': '%'},
                    step=0.1
                )
            ], style={
                'padding-top': '35px'
            }
            ),

            #X軸
            html.P('x Asix:' ,style={'padding':'5px','padding-top': '50px'}),
            html.Div(id='x_axis', children=[
                dcc.Dropdown(
                    id='x_axisVal',
                    options=[{'label': 'OM', 'value': 1},{'label': 'TCM', 'value': 2},{'label': 'Berry Ratiio', 'value': 3}],
                    value=1,
                    style={'padding':'5px','width':'100%'}
                )
            ]),

            #Filter Button
            html.Button('CALCULATE', id='filButton',style={'margin-top': '25px', 'width': '100%', 'height': '10%','color':'white','background-color': '#3a7cef','letter-spacing':'0.1rem'})
            
        ], style={
            'width': 'calc(100%  *1.5/ 10)',
            'height':'80vh',
            'border-radius': '5px',
            'background-color': '#f9f9f9',
            'margin': '10px',
            'padding': '15px',
            'position': 'relative',
            'box-shadow': '2px 2px 2px lightgrey'
                }
        ),


        #3列目
        html.Div(id='Analytics',children=[
                html.P('Graph'),
                dcc.Graph(id='graph', style={'width': '100%', 'display': 'inline-block'})
        ], style={
            'width': 'calc(100% *4/ 10)',
            'border-radius': '5px',
            'background-color': '#f9f9f9',
            'margin': '10px',
            'padding': '15px',
            'position': 'relative',
            'box-shadow': '2px 2px 2px lightgrey'
                }
        ),


        #BMfieled
        html.Div(id='BM',children=[
            #dropdown:BM Companies
            html.P('BM Companies'),
                #company table
                html.Div(id='selectedcompanies',children=[
                    
                ], style={
                    'height': '40vh',
                    'float': 'bottom',
                    'display': 'block',
                    'overflow-x': 'scroll',
                    'border-radius': '5px',
                    'background-color': '#f9f9f9',
                    'margin': '10px',
                    'padding': '15px',
                    'position': 'relative',
                    'box-shadow': '2px 2px 2px lightgrey'
                }),

                #Output Button
                html.Button('Output', id='outputButton',style={'margin-top': '25px', 'width': '100%', 'height': '10%','color':'white','background-color': '#3a7cef','letter-spacing':'0.1rem'})

        ], style={
            'width': 'calc(100% / 5)',
            'border-radius': '5px',
            'background-color': '#f9f9f9',
            'margin': '10px',
            'padding': '15px',
            'position': 'relative',
            'box-shadow': '2px 2px 2px lightgrey'}
        )
    ],style={
        'display': 'flex'
    }
    )
],style={
    'font-size': '1em',
    'line-height': '1.6',
    'font-weight': '400',
    'font-family': '"Open Sans", "HelveticaNeue", "Helvetica Neue", "Helvetica, Arial, sans-serif"',
    'color': 'rgb(50, 50, 50)',
    'margin': '2%'
})

#target company
@app.callback(
    Output(component_id='companyinfo', component_property='children'),
    [Input(component_id='dropdown-target', component_property='value')]
)

def update_target_company(value):
    if value is None or value == '' or not value:
        return
    else:
        df_target = df_master[df_master['Company_Name']==value]
        del df_target['Company_Name']
    return html.Div(generate_table(df_target))


#filter
@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='filButton', component_property='n_clicks')],
    [dash.dependencies.State(component_id='CoveredYearVal', component_property='value'),
     dash.dependencies.State(component_id='StatusVal', component_property='value'),
     dash.dependencies.State(component_id='IndepVal', component_property='value'),
     dash.dependencies.State(component_id='CountryVal', component_property='value'),
     dash.dependencies.State(component_id='USSICVal', component_property='value'),
     dash.dependencies.State(component_id='AvailableYearsVal', component_property='value'),
     dash.dependencies.State(component_id='3yrLossVal', component_property='value'),
     dash.dependencies.State(component_id='ProductVal', component_property='value')]
)

def filtering_data(n_clicks,CoveredYearVal,StatusVal,IndepVal,CountryVal,USSICVal,AvailableYearsVal,yrLossVal,ProductVal):
    fil_df = df_basic.copy()
    if  StatusVal is None or StatusVal == '' or not StatusVal:
        pass
    else:
        fil_df = df_basic[df_basic['Status'].isin(StatusVal)]

    if IndepVal is None or IndepVal == '' or not IndepVal:
        pass
    else:
        fil_df = fil_df[fil_df['Indep'].isin(IndepVal)]

    if CountryVal is None or CountryVal == '' or not CountryVal:
        pass
    else:
        fil_df = fil_df[fil_df['Country'].isin(CountryVal)]

    if USSICVal is None or USSICVal == '' or not USSICVal:
        pass
    else:
        fil_df = fil_df[fil_df['US_SIC_Primary_code(s)_(M)'].isin(USSICVal)]

    if ProductVal is None or ProductVal == '' or not ProductVal:
        y = ''
        pass
    else:
        y = ProductVal

    #最大100
    fil_df = fil_df.iloc[:100]

    #PLI OM 2016~2018 平均
    fil_df['OM'] = (fil_df['Operating Profits Margin_2018']+fil_df['Operating Profits Margin_2017']+fil_df['Operating Profits Margin_2016'])/3
    #横軸
    x = 'OM'
    #x = 'Operating Profits Margin_2018'
    return  make_plot(fil_df, y, x)


#bm companies
@app.callback(
    Output(component_id='selectedcompanies', component_property='children'),
    [Input(component_id='graph', component_property='selectedData')]
)

def update_output_div(input_value):
    if input_value is None or input_value == '' or not input_value:
        dff = fil_df[fil_df['Company_Name']=='']
    else:
        selectedlist = []
        for data in input_value['points']:
            selectedlist += (data['customdata'])
        dff = fil_df[fil_df['Company_Name'].isin(selectedlist)]


    return html.Div(generate_table(dff))

if __name__ == '__main__':
    app.run_server(debug=True)
