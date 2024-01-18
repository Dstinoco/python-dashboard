from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

df=pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv")
country = ['Brazil', 'United States', 'Venezuela', 'Argentina']
df = df.loc[df['country'].isin(country)]
df = df[df.year >= 1997]


app = Dash(__name__)


app.layout = html.Div([
   dcc.Graph(id='graph-with-slider'), 
   dcc.Slider(
       id='year-slide',
       min=df['year'].min(),
       max=df['year'].max(),
       value=df['year'].min(),
       marks={str(year): str(year) for year in df['year'].unique()},
       step=None
   ),
   
   html.Div([
   dcc.Dropdown(id='drop',
            options=[{"label":"Espectativa de Vida", 'value': 'lifeExp'},
                     {"label":"População", 'value': 'pop'},
                     {"label":"PIB per capita ", 'value': 'gdpPercap'},
                     ],
            value='lifeExp'
                 ),
   
   dcc.Dropdown(id='drop2',
            options=country,
            value='Brazil'
                 ),
   html.Button(id='btn', children='Filtrar'),
   
   dcc.Graph(id='fig2')
]),
   
   
])


@app.callback(
    Output("graph-with-slider", "figure"),
    [Input("year-slide", 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    
    fig = px.scatter(filtered_df, x='gdpPercap', y='lifeExp', size='pop', color='country',
                     log_x=True, size_max=55)
    
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('fig2',"figure"),
      Input('btn', 'n_clicks'),
        State(component_id='drop', component_property='value'),
        State(component_id='drop2', component_property='value'),
     
    prevent_initial_call=False)
def update_brasil(btn, value, pais):
    brasil = df[df['country']== pais]
    fig2 = px.bar(brasil, x=value, y='year', color='country')
    return fig2
    


















if __name__ == '__main__':
    app.run_server(debug=True)