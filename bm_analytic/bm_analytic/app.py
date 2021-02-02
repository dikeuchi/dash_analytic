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

from functions import *

#Import Comanies Data
df_basic = pd.read_csv('../bm_analytic/data/BM_DataSet_1000.csv', index_col=0)
#global dataframe, filter
fil_df = df_basic.copy()
#master info
df_master = df_basic[['Company_Name','Country','City','Website','Status','Indep','Number_of_employees_2018','US_SIC_Primary_code(s)_(M)','Main_activity','Primary_business_line','Full_overview']]

#option
indep = df_master['Indep'].unique()
indep.sort()
country = df_master['Country'].unique()
country.sort()
ussic = df_master['US_SIC_Primary_code(s)_(M)'].unique()
ussic.sort()
mainactivity = df_master['Main_activity'].str.split('; ', expand=True)
mainactivity = mainactivity[0].dropna().unique()

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
            html.Div(id='RDsales',children=[
                daq.Slider(
                    id='RDsalesVal',
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
                    options=[{'label': 'OM', 'value': 'OM'},{'label': 'TCM', 'value': 'TCM'},{'label': 'BerryRatio', 'value': 'BerryRatio'}],
                    value='OM',
                    style={'padding':'5px','width':'100%'}
                )
            ]),

            #Filter Button
            html.Button('SEARCH', id='filButton',style={
                'margin-top': '25px',
                'width': '100%',
                'height': '10%',
                'color':'white',
                'background-color': '#3a7cef',
                'letter-spacing':'0.1rem',
                'font-size':'large'
                })
            
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
                    'height': '60vh',
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
     dash.dependencies.State(component_id='ProductVal', component_property='value'),
     dash.dependencies.State(component_id='MainactivityVal', component_property='value'),
     dash.dependencies.State(component_id='RDsalesVal', component_property='value'),
     dash.dependencies.State(component_id='SGAsalesVal', component_property='value'),
     dash.dependencies.State(component_id='x_axisVal', component_property='value')
     ]
)

def filtering_data(n_clicks,CoveredYearVal,StatusVal,IndepVal,CountryVal,USSICVal,AvailableYearsVal,yrLossVal,ProductVal,MainactivityVal,RDsalesVal,SGAsalesVal,x_axisVal):
    global fil_df
    fil_df = df_basic.copy()
    
    #Covered Year
    YearSpan= CoveredYearVal[1]+1 - CoveredYearVal[0]

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
    
    if MainactivityVal is None or MainactivityVal == '' or not MainactivityVal:
        pass
    else:
        fil_df = fil_df[fil_df['Main_activity'].isin(MainactivityVal)]

    #R&D/sales = Research_&_Development_expenses ÷ Operating_Revenue_/_Turnover
    if RDsalesVal is None or RDsalesVal == '' or not RDsalesVal or 0:
        pass
    else:
        fil_df = fil_df.assign(RDsales_total=0)
        for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
            fil_df['RDsales_total'] = fil_df['RDsales_total'] + (fil_df['Research_&_Development_expenses_th_LCU_' + str(i)] / fil_df['Operating_Revenue_/_Turnover_th_LCU_' + str(i)])
        fil_df['RD/sales'] = fil_df['RDsales_total']/(YearSpan)
        # filter
        fil_df = fil_df[fil_df['RD/sales'] <= RDsalesVal/100]

    #SGA/sales = SGA ÷ Operating_Revenue_/_Turnover
    if SGAsalesVal is None or SGAsalesVal == '' or not SGAsalesVal or 0:
        pass
    else:
        fil_df = fil_df.assign(SGAsales_total=0)
        for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
            fil_df['SGAsales_total'] = fil_df['SGAsales_total'] + (fil_df['SGA_' + str(i)] / fil_df['Operating_Revenue_/_Turnover_th_LCU_' + str(i)])
        fil_df['SGA/sales'] = fil_df['SGAsales_total']/(YearSpan)
        # filter
        fil_df = fil_df[fil_df['SGA/sales'] <= SGAsalesVal/100]

    #最大100
    fil_df = fil_df.iloc[:100]

    #PLI OM = Operating Profit ÷ Operating Revenue 
    fil_df['OM_total'] = 0
    for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
        fil_df['OM_total'] = fil_df['OM_total'] + fil_df['Operating Profits Margin_' + str(i)]
    fil_df['OM'] = fil_df['OM_total']/(YearSpan)
    #PLI TCM = Operating P/L ÷ (Operating Revenue - Operating P/L)
    fil_df['TCM_total'] = 0
    for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
        fil_df['TCM_total'] = fil_df['TCM_total'] + fil_df['Total Cost-Markup_' + str(i)]
    fil_df['TCM'] = fil_df['TCM_total']/(YearSpan)
    #Berry Ratio = Gross Profit ÷ Selling, General & Administrative Expenses
    fil_df['BerryRatio_total'] = 0
    for i in range(CoveredYearVal[0],CoveredYearVal[1]+1):
        fil_df['BerryRatio_total'] = fil_df['BerryRatio_total'] + fil_df['Berry Ratio_' + str(i)]
    fil_df['BerryRatio'] = fil_df['BerryRatio_total']/(YearSpan)

    #横軸
    if x_axisVal is None or x_axisVal == '' or not x_axisVal:
        pass
    else:
        #default = OM
        x = x_axisVal
    
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

        output_table = dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in dff.columns],
            data=dff.to_dict('records'),
            fixed_rows={ 'headers': True, 'data': 0 },
            style_table={
                'border': 'thin light solid',
                'white-space': 'nowrap',
                },
            style_cell={
                'padding':'5px',
                'minWidth':'80px',
                'textAlign':'left',
                'font_family':'Arial'
                },
            style_header={
                'background-color':'rgb(116,116,128)',
                'color':'white'
                },
            export_format='csv',
        )

        return output_table


if __name__ == '__main__':
    app.run_server(debug=True)
