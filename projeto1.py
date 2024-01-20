from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


df_data = pd.read_csv('supermarket_sales.csv')
df_data['Date'] = pd.to_datetime(df_data['Date'])

load_figure_template('darkly')

app = Dash(
    external_stylesheets=[dbc.themes.DARKLY]
)
server = app.server

# ==========  Layout  ========= #

app.layout = html.Div(children=[

    dbc.Row([

        dbc.Col([

            dbc.Card([

                html.H3("Tinoco #1", id='title'),
                html.Hr(),
                html.H3("Cidades:"),
                dcc.Checklist(df_data["City"].unique(),
                value= df_data["City"].unique(), id='check_city'),
                html.Hr(),
                html.H5('Variável de análise'),
                dcc.RadioItems(['gross income', 'Rating'], 'gross income', id='main_variable')

            ], id='card1')
        ], sm=2),

        dbc.Col([


                dbc.Row([
                    dbc.Col([dcc.Graph(id='city_fig')], sm=4),
                    dbc.Col([dcc.Graph(id='pay_fig')], sm=4),
                    dbc.Col([dcc.Graph(id='gender_fig')], sm=4)
                ]),
                dbc.Row([dcc.Graph(id='date_fig')]),
                dbc.Row([dcc.Graph(id='income_per_product_fig')])       
                                         
                
        ], sm=10)
    ])




])



# ==========  Callbacks  ========= 
@app.callback(
    [Output('city_fig', 'figure'),
     Output('pay_fig', 'figure'),
     Output('gender_fig', 'figure'),
     Output('date_fig', 'figure'),
     Output('income_per_product_fig', 'figure')
     
     ],
    [
    Input('check_city', 'value'),
    Input('main_variable', 'value')
    ])
def render_grafh(cities, main_variable):
    df_filtered = df_data[df_data['City'].isin(cities)]

    if main_variable == 'Rating':
        df_city = df_filtered.groupby('City')[[main_variable]].mean().reset_index()
        df_pay = df_filtered.groupby('Payment')[[main_variable]].mean().reset_index() 
        df_gender = df_filtered.groupby(['Gender', 'City'])[[main_variable]].mean().reset_index()
        df_date = df_filtered.groupby('Date')[[main_variable]].mean().reset_index()    
        df_product = df_filtered.groupby(['Product line', 'City'])[[main_variable]].mean().reset_index()
    else:
        df_city = df_filtered.groupby('City')[[main_variable]].sum().reset_index()
        df_pay = df_filtered.groupby('Payment')[[main_variable]].sum().reset_index()   
        df_gender = df_filtered.groupby(['Gender', 'City'])[[main_variable]].mean().reset_index()
        df_date = df_filtered.groupby('Date')[[main_variable]].mean().reset_index()    
        df_product = df_filtered.groupby(['Product line', 'City'])[[main_variable]].sum().reset_index()


    city_fig = px.bar(df_city, x='City', y=main_variable)
    pay_fig = px.bar(df_pay, y='Payment', x=main_variable)
    product_fig = px.bar(df_product, y='Product line', x=main_variable, color='City', orientation='h', barmode='group')
    gender_fig = px.bar(df_gender, x='Gender', y=main_variable, color='City', barmode='group')
    date_fig = px.bar(df_date, x='Date', y=main_variable)



    for fig in [city_fig, pay_fig, gender_fig, date_fig]:
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template='darkly')

    product_fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500, template='darkly')


    return city_fig, pay_fig, gender_fig, date_fig, product_fig






# ==========  Run server  ========= 
if __name__ == '__main__':
    app.run_server(debug=True)
