import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv')

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
    # Get the latest data from the CSV file
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv')

    # Create a line chart with Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines'))

    # Set the chart title and axis labels
    fig.update_layout(title='Ethereum Price', xaxis_title='Date', yaxis_title='Price')

    return fig

@app.callback(
    Output('data-table', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_table(n):
    # Get the latest data from the CSV file
    df = pd.read_csv('/home/ubuntu/proj/eth_prices.csv')

    # Create a HTML table with the latest data
    table = html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        # Body
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(len(df), 10))]
    )

    return table

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
