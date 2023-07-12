from coinbase.wallet.client import Client
from dotenv import load_dotenv
import os
import traceback

load_dotenv()
apikey = os.getenv('KEY')
apisecret= os.getenv('SECRET')

client = Client(apikey, apisecret)

symbol = "LTC"

# Get the account id details
try:
    #print(client.get_primary_account())
    account = client.get_account(symbol)
    for key, value in account.items():
        if key == "id":
            accountid = value
            return_result = client.buy(accountid, amount='0.1249667', currency=symbol, commit=True)
            print(return_result)
except Exception as e:
    # Print the exception as text
    traceback.print_exc()
    accountid = "None"
    pass
