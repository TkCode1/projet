```
url="https://ethereumprice.org/live/"
html=$(curl -s "$url")
price=$(echo "$html" | grep -m1 -o '<span class="value">[^<]*</span>' | sed -e 's/<[^>]*>//g' )
echo "The Ethereum price is: $price"
timestamp=$(date +"%Y-%m-%dT%H:%M:%SZ")
echo "$timestamp;$price" | awk -F ';' '{print $1 ";" $2}' >> eth_prices.csv
```
