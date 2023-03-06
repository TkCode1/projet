import dash
from dash import dcc
from dash import html
import pandas as pd

# Load the CSV file containing the ETH price data
df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], sep = ';')

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Ethereum Price Over Time'),

    # Add a graph showing the price of ETH over time
    dcc.Graph(
        id='price-graph',
        figure={
            'data': [
                {'x': df['date'], 'y': df['price'], 'type': 'line', 'name': 'ETH price'},
            ],
            'layout': {
                'title': 'ETH Price over Time',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Price ($)'}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
