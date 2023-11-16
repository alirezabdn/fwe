import time
import pandas as pd
import pandas_ta as ta
import ccxt

# Initialize your account balance in USDT
initial_balance = 19541.94

# + create exchange
# + if need to buy/sell
# `
exchange = ccxt.lbank2({
    "apiKey": '9cb64935-dc67-49a8-a2d3-472d5df03d20',
    "secret": '9BE6F7AD3E448E0B596421ECCFBA14FF'
})
# `
exchange = ccxt.lbank2()

def get_ohlcv(symbol, interval='1m', limit=10) -> pd.DataFrame:
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    bars = exchange.fetch_ohlcv(symbol, timeframe=interval, limit=limit)
    df = pd.DataFrame(bars, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

if __name__ == '__main__':
    symbol = 'ETH/USDT'  # Use Ethereum (ETH) against USDT
    quantity = 1.0
    balance = initial_balance
    bought = False
    
    print('bot is started!')
    
    while True:
        dataframe = get_ohlcv(symbol, limit=100)
        last_row = len(dataframe.index) - 2
        
        dataframe['signal'] = ta.supertrend(dataframe['high'], dataframe['low'], 
                                            dataframe['close'], 8, 2)['SUPERTd_8_2.0']
        
        current_price = dataframe['close'][last_row]
        current_time = dataframe['timestamp'][last_row]
        
        if not bought:
            if dataframe['signal'][last_row] == 1:
                print(f'buy signal for {symbol} on {current_price} at {current_time}')
                # Calculate the cost of buying 1 ETH
                cost = current_price * quantity
                if cost <= balance:
                    balance -= cost
                    bought = True
                    print(f'Balance after purchase: {balance} USDT')
                else:
                    print('Insufficient balance for purchase')
        
        else:
            if dataframe['signal'][last_row] == -1:
                print(f'sell signal for {symbol} on {current_price} at {current_time}')
                # Calculate the revenue from selling 1 ETH
                revenue = current_price * quantity
                balance += revenue
                bought = False
                print(f'Balance after sale: {balance} USDT')
        
        time.sleep(60)
