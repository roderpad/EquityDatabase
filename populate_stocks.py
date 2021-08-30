import config
import config_forGithub
import alpaca_trade_api as tradeapi
import psycopg2
import psycopg2.extras

#* Establish connection to postgreSQL database
connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
#connection = psycopg2.connect(host=config_forGithub.DB_HOST, database=config_forGithub.DB_NAME, user=config_forGithub.DB_USER, passwd=config_forGithub.DB_PASS)

#* Cursor is used to execute queries against the database
#cursor = connection.cursor()
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) #* Allows you to access database returns as a dictionary rather than a tuple.

#* Example query:
# cursor.execute("SELECT * FROM stock")

#* Example retrieval of results:
#stocks = cursor.fetchall()
#for stock in stocks:
#    print(stock['symbol'])

#* Connect to Alpaca (Paper Trading, in this case) API
api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)
#api = tradeapi.REST(config_forGithub.API_KEY, config_forGithub.API_SECRET, base_url=config_forGithub.API_URL)

#* Get Alpaca API available assets
assets = api.list_assets()
#print(assets)

#* Insert assets into database
for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable:
            #print(f"Inserting stock {asset.name} {asset.symbol}")
            cursor.execute("""
                INSERT INTO stock (name, symbol, exchange, is_etf)
                VALUES (%s, %s, %s, false)          
                """, (asset.name, asset.symbol, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)

#* Commit database changes to the database. 
connection.commit()