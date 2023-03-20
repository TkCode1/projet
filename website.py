import dash
from dash import dcc
from dash import html
import pandas as pd
import time
import datetime

# Load the CSV file containing the ETH price data
df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price', 'open_price', 'close_price'], sep=';')

# Get the last row of the DataFrame
last_row = df.tail(1)

# Get the current ETH price from the last row
current_price = last_row['price'].values[0]

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app with the interval component
app.layout = html.Div(children=[
    html.Img(src='https://logo-marque.com/wp-content/uploads/2020/12/Ethereum-Logo.png', style={'width': '200px', 'display': 'block', 'margin': '0 auto'}),
    #html.H1(children=f'ETH last price: ${current_price}'),
    #changes
    html.H1(id='current-price', style={'text-align': 'center', 'color': '#627EEA'}),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000, # in milliseconds
        n_intervals=0
    ),
    # Add a graph showing the price of ETH over time
    dcc.Graph(
        id='price-graph',
        figure={
            'data': [
                {'x': df['date'], 'y': df['price'], 'type': 'line', 'name': 'ETH price', 'line': {'color': '#627EEA'}},
            ],
            'layout': {
                'title': 'ETH Price over Time',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Price ($)'}
            }
        }
    ),
    # Add a tab for daily price information
    dcc.Tabs(id='price-info-tabs', value='tab-1', children=[
        dcc.Tab(label='Price History', value='tab-1', children=[
            dcc.Graph(
                id='history-graph',
                figure={
                    'data': [
                        {'x': df['date'], 'y': df['close_price'], 'type': 'line', 'name': 'Close price', 'line': {'color': '#EF553B'}},
                        {'x': df['date'], 'y': df['open_price'], 'type': 'line', 'name': 'Open price', 'line': {'color': '#00CC96'}}
                    ],
                    'layout': {
                        'title': 'ETH Price History',
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': 'Price ($)'}
                    }
                }
            ),
        ]),
    ]),
])

# Define the function to update the current price display
@app.callback(
    dash.dependencies.Output('current-price', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_current_price(n):
    # Load the updated CSV file containing the ETH price data
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price', 'open_price', 'close_price'], sep=';')
    # Get the last row of the DataFrame
    last_row = df.tail(1)
    # Get the current ETH price from the last row
    current_price = last_row['price'].values[0]
    # Return the updated current price display
    return f'ETH last price: ${current_price}'

if __name__ == '__main__':
    app.run_server(debug=True, host
