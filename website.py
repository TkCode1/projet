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


def update_daily_price_tab():
    # Get yesterday's date in UTC+1 timezone
    tz = pytz.timezone('Europe/Paris')
    yesterday = datetime.now(tz) - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    # Read the csv file
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', parse_dates=['timestamp'])

    # Filter data for yesterday's date
    yesterday_data = df[df['timestamp'].dt.date == yesterday.date()]

    if yesterday_data.empty:
        print(f"No data for {yesterday_str}")
        return

    # Get the last row of yesterday's data
    last_row = yesterday_data.tail(1)

    # Display the open and close prices for yesterday's midnight
    open_price = last_row.iloc[0]['price']
    close_price = df[df['timestamp'].dt.date == datetime.now(tz).date()].iloc[0]['price']
    print(f"Daily Price Information for {yesterday_str}\n")
    print(f"Open: {open_price}")
    print(f"Close: {close_price}")


# Define the function to update the daily price information tab
@app.callback(
    dash.dependencies.Output('daily-price-content', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)

def update_daily_price_tab(n):
    # Get yesterday's date in the UTC+1 timezone
    tz = datetime.timezone(datetime.timedelta(hours=1))
    yesterday = datetime.datetime.now(tz).date() - datetime.timedelta(days=1)
    
    # Filter the DataFrame to get yesterday's data
    yesterday_data = df[df['date'] == yesterday.isoformat()]
    
    if len(yesterday_data) == 0:
        # Return a message indicating that there is no data for yesterday
        return html.Div([
            html.H2(f'Daily Price Information for {yesterday}'),
            html.P('No data for yesterday.')
        ])
    else:
        # Get the open and close prices of yesterday
        open_price = yesterday_data['price'].iloc[0]
        close_price = yesterday_data['price'].iloc[-1]
        # Return the updated daily price information
        return html.Div([
            html.H2(f'Daily Price Information for {yesterday}'),
            html.P(f'Open price (midnight UTC+1): {open_price}'),
            html.P('No close price available.')
        ])



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
