import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the CSV file once and store it in memory as a dataframe
df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv')

# Define the Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Ethereum Price Dashboard'),
    dcc.Graph(id='graph'),
    html.Div(id='data-table'),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)
], style={'font-family': 'sans-serif'})

@app.callback(
    Output('graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    # Get the latest data from the dataframe
    latest_df = df.tail(100) # get the last 100 rows
    x = latest_df['timestamp']
    y = latest_df['price']
    
    # Create a line chart with Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines'))

    # Set the chart title and axis labels
    fig.update_layout(title='Ethereum Price', xaxis_title='Timestamp', yaxis_title='Price')

    return fig

@app.callback(
    Output('data-table', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_table(n):
    # Get the latest data from the dataframe
    latest_df = df.tail(10) # get the last 10 rows
    
    # Create a HTML table with the latest data
    table = html.Table(
        # Header
        [html.Tr([html.Th(col) for col in latest_df.columns])] +
        # Body
        [html.Tr([html.Td(latest_df.iloc[i][col]) for col in latest_df.columns]) for i in range(len(latest_df))]
    )

    return table

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
