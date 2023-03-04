import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

url = 'ssh://ec2-user@52.87.232.152/home/ec2-user/ethereum_price.csv'
df = pd.read_csv(url)
print(df.head())

app = dash.Dash(__ethprice__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Ethereum Price'),
    html.Table(
        # Create the table headers
        [html.Tr([html.Th(col) for col in df.columns])] +

        # Create the table rows
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))]
    )
])

# Run the app
if __ethprice__ == '__main__':
    app.run_server(debug=True)
