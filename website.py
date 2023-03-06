import dash
from dash import dcc
from dash import html
import pandas as pd
import time

# Load the CSV file containing the ETH price data
df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], sep=';')

# Get the last row of the DataFrame
last_row = df.tail(1)

# Get the current ETH price from the last row
current_price = last_row['price'].values[0]

# Create a Dash app
app = dash.Dash(__name__)

# Get the low, high, open, and close prices for the day
today = datetime.datetime.today().strftime('%Y-%m-%d')
today_df = df[df['date'] == today]
low_price = today_df['price'].min()
high_price = today_df['price'].max()
open_price = today_df.iloc[0]['price']
close_price = today_df.sort_values(['date', 'price'], ascending=[False, False]).iloc[0]['price']
volatility = today_df['price'].std()

# Define the layout of the app with the interval component
app.layout = html.Div(children=[
    html.Img(src='https://logo-marque.com/wp-content/uploads/2020/12/Ethereum-Logo.png', style={'width': '200px'}),
    html.H1(children=f'ETH last price: ${current_price}'),
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
                {'x': df['date'], 'y': df['price'], 'type': 'line', 'name': 'ETH price'},
            ],
            'layout': {
                'title': 'ETH Price over Time',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Price ($)'}
            }
        }
    ),
    
    dcc.Tab(label='Summary', children=[
        html.H3('Summary of ETH Prices Today', style={'color': 'white'}),
        html.Table([
            html.Thead(html.Tr([html.Th('Price'), html.Th('Value')])),
            html.Tbody([
                html.Tr([html.Td('Low'), html.Td(id='low-price')]),
                html.Tr([html.Td('High'), html.Td(id='high-price')]),
                html.Tr([html.Td('Open'), html.Td(id='open-price')]),
                html.Tr([html.Td('Close'), html.Td(id='close-price')]),
                html.Tr([html.Td('Volatility'), html.Td(id='volatility')]),
            ])
        ])
    ])
])

# Define the function to update the graph data
@app.callback(dash.dependencies.Output('price-graph', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])

# Define the function to update the graph data and summary tab data
@app.callback([dash.dependencies.Output('price-graph', 'figure'),
               dash.dependencies.Output('low-price', 'children'),
               dash.dependencies.Output('high-price', 'children'),
               dash.dependencies.Output('open-price', 'children'),
               dash.dependencies.Output('close-price', 'children'),
               dash.dependencies.Output('volatility', 'children')],
              [dash.dependencies.Input('interval-component', 'n_intervals')])

def update_graph_data(n):
    # Load the updated CSV file containing the ETH price data
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv', names=['date', 'price'], sep=';')
    # Return the updated figure
    return {
        'data': [
            {'x': df['date'], 'y': df['price'], 'type': 'line', 'name': 'ETH price'},
        ],
        'layout': {
            'title': 'ETH Price over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price ($)'}
        }
    }



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
