import requests
import pandas

def get_crypto_info(count:int) -> str:
    """return html code of table contain needed data"""
    print("Getting latest Crypto Info...")
    response = requests.get("https://coinmarketcap.com/")
    print("Crypto Info Successfully Saved!")
    return pandas.read_html(response.text)[0][:count+1][["Name", "Price", "24h %", "7d %", "Market Cap"]].to_html()

