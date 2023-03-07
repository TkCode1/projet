import dash
from dash import dcc
from dash import html
import pandas as pd
import time
import datetime

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
    dcc.Tabs(id='daily-price-tab', value='tab-1', children=[
        dcc.Tab(label='Daily Price Information', value='tab-1', children=[
            html.Div(id='daily-price-content'),
        ]),
    ]),
])
#changes
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

# Define the function to update the daily price information tab
@app.callback(
    dash.dependencies.Output('daily-price-content', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)

def update_daily_price_tab(n):
    # Get today's date
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    print(f'Today: {today}')
    # Get today's data from the DataFrame
    today_data = df[df['date'] == today]
    print(f'Today data: {today_data}')
    # Check if today_data is empty
    if len(today_data) == 0:
        # Return a message indicating that there is no data for today
        return html.Div([
            html.H2(f'Daily Price Information for {today}'),
            html.P('No data for today.')
        ])
    else:
        # Get the open and close prices of the day
        open_price = today_data['price'].iloc[0]
        close_price = today_data['price'].iloc[-1]
        # Return the updated daily price information
        return html.Div([
            html.H2(f'Daily Price Information for {today}'),
            html.P(f'Open price: {open_price}'),
            html.P(f'Close price: {close_price}')
        ])



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
