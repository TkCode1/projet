import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], header=None)

fig = px.line(df, x='date', y='price', title='Ethereum Price')

app.layout = html.Div(children=[
    html.H1(children='Ethereum Price Graph'),
    dcc.Graph(
        id='eth-price-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
