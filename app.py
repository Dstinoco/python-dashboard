from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State



app = Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

fig = px.bar(df, x='year', y='pop', color='country')




#==============================================
app.layout = html.Div(id='div1',
    children=[
        html.H1("Hellow Dash!", id='h1'),

        html.Div("Dash com python", id='texto1'),

        html.Label('Estados', id='texto2'),
        dcc.Dropdown(
            id='dp1',
            options=['ES', 'MG', 'SP', 'RJ'],
            value='ES'),

        html.Div(['Entrada', 
                  dcc.Input(id='my-input', value='Valor inicial', type="text")]),
        html.Br(),
        html.Div(id='my-output'),
        
        

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

@app.callback(
    Output(component_id='my-output', component_property="children"),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(value):
    return 'saida: {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)