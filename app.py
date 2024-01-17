from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px



app = Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

fig = px.bar(df, x='year', y='pop', color='country')




#==============================================
app.layout = html.Div(id='div1',
    children=[
        html.H1("Hellow Dash!", id='h1'),

        html.Div("Dash com python"),

        dcc.Dropdown(
            id='dp1',
            options=['ES', 'MG', 'SP', 'RJ'],
            value='ES'),

        

        dcc.Checklist(
            id='check',
            options=[
                {"label": 'Brasil', "value": "Brasil"},
                {"label": 'Estados Unidos', "value": "EUA"},
                {"label": 'Alemanha', "value": "Alemanha"},

            ],
            value=['Brasil']
        ),

        dcc.Graph(figure=fig, id='graph')
    ]
)



if __name__ == '__main__':
    app.run_server(debug=True)