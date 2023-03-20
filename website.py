import dash
from dash import dcc
from dash import html
import pandas as pd
import datetime
import time

# Load the CSV file containing the ETH price data
df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], sep=';')

# Get the last row of the DataFrame
last_row = df.tail(1)

# Get the current ETH price from the last row
current_price = last_row['price'].values[0]

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app with the interval component
app.layout = html.Div(children=[
    html.Img(src='https://logo-marque.com/wp-content/uploads/2020/12/Ethereum-Logo.png', style={'width': '200px', 'display': 'block', 'margin': '0 auto'}),
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
    html.Div(
    id='price-report',
    style={'text-align': 'center', 'margin-top': '20px'}
    ),
])

# Define the function to update the current price display
@app.callback(
    dash.dependencies.Output('current-price', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_current_price(n):
    # Load the updated CSV file containing the ETH price data
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], sep=';')
    # Get the last row of the DataFrame
    last_row = df.tail(1)
    # Get the current ETH price from the last row
    current_price = last_row['price'].values[0]
    # Return the updated current price display
    return f'ETH last price: ${current_price}'

# Define the function to update the graph data
@app.callback(dash.dependencies.Output('price-graph', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_graph_data(n):
    # Load the updated CSV file containing the ETH price data
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], sep=';')
    # Return the updated figure
    return {
        'data': [
            {'x': df['date'], 'y': df['price'], 'type': 'line', 'name': 'ETH price', 'line': {'color': '#627EEA'}},
        ],
        'layout': {
            'title': 'ETH Price over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price ($)'}
        }
    }

def update_price_report():
    # Load the CSV file containing the ETH price data
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], sep=';')
    # Get the date of yesterday at 23:55
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=55, second=0, microsecond=0)
    # Get the date of today at 00:00
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # Get the close price of yesterday and the open price of today
    yesterday_close = df[df['date'] == yesterday.strftime('%Y-%m-%d %H:%M:%S')]['price'].values[0]
    print(yesterday_close)
    today_open = df[df['date'] == today.strftime('%Y-%m-%d %H:%M:%S')]['price'].values[0]
    # Return the price report
    return f'Yesterday close price: ${yesterday_close} - Today open price: ${today_open}'

@app.callback(
    dash.dependencies.Output('price-report', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)

def update_price_report_callback(n):
    # Get the current time
    now = datetime.datetime.now()
    # If it is 20:00 or later, update the price report
    if now.hour >= 11:
        return update_price_report()
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
