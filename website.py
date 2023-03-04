import pandas as pd

url = 'ssh://ec2-user@52.87.232.152/home/ec2-user/ethereum_price.csv'
df = pd.read_csv(url)
print(df.head())
