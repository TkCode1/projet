import dash
from dash import dcc
from dash import html
import pandas as pd
import datetime
import time
import pytz

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
    # Add a Div to display the report under the graph
    html.Div(id='daily-report', style={'text-align': 'center', 'color': '#627EEA'})
])

# Define the function to update the current price display
@app.callback(
    dash.dependencies.Output('current-price', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])

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

# Define a function to determine whether it's 8 pm or later
def is_time_to_update():
    local_time = datetime.datetime.now(pytz.timezone('UTC'))
    return local_time.hour >= 10

# Define the function to update the daily report
@app.callback(
    dash.dependencies.Output('daily-report', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_daily_report(n):
    if not is_time_to_update():
        return dash.no_update

    # Load the updated CSV file containing the ETH price data
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], sep=';')

    # Convert the date column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # Calculate the open price of the current day and the close price of the last day
    now = datetime.datetime.now(pytz.timezone('UTC'))
    today = now.date()
    yesterday = today - datetime.timedelta(days=1)

    # Get the open price for the current day
    open_price_today = df[df['date'].dt.date == today].iloc[0]['price']

    # Get the close price for the last day
    close_price_yesterday = df[df['date'].dt.date == yesterday].iloc[-1]['price']

    # Return the updated daily report
    return f"Open price today: ${open_price_today:.2f} | Close price yesterday: ${close_price_yesterday:.2f}"


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
