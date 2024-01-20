from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


df_data = pd.read_csv('supermarket_sales.csv')
df_data['Date'] = pd.to_datetime(df_data['Date'])

app = Dash(__name__)
server = app.server

# ==========  Layout  ========= #

app.layout = html.Div([
    html.H3("Cidades:"),
    dcc.Checklist(df_data["City"].unique(),
          value= df_data["City"].unique(), id='check_city'),

    html.H5('Variável de análise'),
    dcc.RadioItems(['gross income', 'Rating'], 'gross income', id='main_variable'),
    

    dcc.Graph(id='city_fig'),
    dcc.Graph(id='pay_fig'),
    dcc.Graph(id='income_per_product_fig')

])



# ==========  Callbacks  ========= 
@app.callback(
    [Output('city_fig', 'figure'),
     Output('pay_fig', 'figure'),
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
        df_product = df_filtered.groupby(['Product line', 'City'])[[main_variable]].mean().reset_index()
    else:
        df_city = df_filtered.groupby('City')[[main_variable]].sum().reset_index()
        df_pay = df_filtered.groupby('Payment')[[main_variable]].sum().reset_index()    
        df_product = df_filtered.groupby(['Product line', 'City'])[[main_variable]].sum().reset_index()

    city_fig = px.bar(df_city, x='City', y=main_variable)
    pay_fig = px.bar(df_pay, y='Payment', x=main_variable)
    product_fig = px.bar(df_product, y='Product line', x=main_variable, color='City', orientation='h', barmode='group')

    city_fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    pay_fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    product_fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500)


    return city_fig, pay_fig, product_fig






# ==========  Run server  ========= 
if __name__ == '__main__':
    app.run_server(debug=True)
