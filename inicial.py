from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State




app = Dash(__name__)














if __name__ == '__main__':
    app.run_server(debug=True)
