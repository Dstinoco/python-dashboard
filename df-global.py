from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State




app = Dash(__name__)



df = pd.DataFrame({
    'id_estudante': range(1, 11),
    "score": [1, 3, 3, 2 , 5, 4 , 2, 3, 5, 4]
})



app.layout = html.Div([
    dcc.Dropdown(list(range(1, 6)), 1, id='score'),
    "Foi pontuado pela seguinte quantidade de estudantes:",
    html.Div(id='output'),
    dcc.Store(id='store')
])


@app.callback(
    Output('store', 'data'),
    Input('score', 'value')
    )
def update_output(value):
    filtered_df = df[df['score'] == value]
    return filtered_df.to_dict()
    


@app.callback(
    Output('output', 'children'),
    Input('store', 'data')
)
def update_out(data):
    filtered_df = pd.DataFrame(data)
    return len(filtered_df)
    
    
if __name__ == '__main__':
    app.run_server(debug=True)
