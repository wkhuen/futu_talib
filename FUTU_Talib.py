from futu import *
import futu as ft
import talib
import pandas as pd
import matplotlib.pyplot as plt

#PS C:\Users\wkhue\PycharmProjects\FUTU> pip install C:\Users\wkhue\Downloads\TA_Lib-0.4.21-cp39-cp39-win_amd64.whl
#Processing c:\users\wkhue\downloads\ta_lib-0.4.21-cp39-cp39-win_amd64.whl
#Installing collected packages: TA-Lib
#Successfully installed TA-Lib-0.4.21

symbol = 'HK.00388'
quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111, is_encrypt=False) #OK!! 2021.09.01 12:55am
start_dt = datetime.today()-timedelta(365)
end_dt = datetime.today()-timedelta(0)
start_dt_str = start_dt.strftime("%Y-%m-%d")
end_dt_str = end_dt.strftime("%Y-%m-%d")
#print(quote_ctx.get_market_snapshot(['HK.00700','HK.00388']))

ret, data, page_req_key = quote_ctx.request_history_kline(symbol, start=start_dt_str, end=end_dt_str, max_count=999999)
if ret == RET_OK:
    print('1:', data)
    #print('2:', data['code'][0])    # 取第一条的股票代码
    #print('3:', data['close'].values.tolist())   # 第一页收盘价转为 list
else:
    print('error:', data)
    quit()

#print ("HEAD: ", data.columns.values.tolist())
#HEAD:  ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume', 'turnover', 'change_rate', 'last_close']

#integer = CDLENGULFING(open, high, low, close)
#data_clean = data.iloc[:, [1,2,4,5,3]]
#data_clean.to_csv('data_clean.csv')
#print('DATA_CLEAN:', data_clean)
morning_star = talib.CDLMORNINGSTAR(data['open'], data['high'], data['low'], data['close'], penetration=0)
#print('Morning Star: ', morning_star[morning_star!=0])
engulfing =  talib.CDLENGULFING(data['open'], data['high'], data['low'], data['close'])
#print('Engulfing: ', engulfing[engulfing!=0])
three_crows = talib.CDL3BLACKCROWS(data['open'], data['high'], data['low'], data['close'])
print('3_Black_Crows: ', three_crows)



sma_fast = talib.SMA(data['close'].values, 15)
sma_slow = talib.SMA(data['close'].values, 30)
sma_diff = (sma_fast-sma_slow)/sma_fast

plt.plot(sma_fast, label='sma_fast')
plt.plot(sma_slow, label='sma_slow')
plt.plot(data['close'].values,'--',label='Price '+symbol)
plt.legend(loc='best')
#plt.show()

for i in range(len(data)):
    if sma_diff [i] > 0.03:
        plt.plot(i, data['close'].values[i], 'g.')
    elif sma_diff[i] < -0.03:
        plt.plot(i, data['close'].values[i], 'r.')
    else:
        plt.plot(i, data['close'].values[i], 'b.') #Neutral
plt.show()


macd, macdsignal, macdhist = talib.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)

print ('macdsignal: ', macdsignal)

data['Morning Star'] = morning_star
data['Engulfing'] = engulfing
data['Three_crows'] = three_crows
data['MACD'] = macd
data.to_csv(symbol + '.csv')
#print ('Final Data:', data)

morning_star_days = data[data['Morning Star'] != 0]
print('Morning Star Days:', morning_star_days)

engulfing_days = data[data['Engulfing'] != 0]
print('Engulfing Days:', engulfing_days)

three_crows_days = data[data['Three_crows'] != 0]
print('Three_crows Days:', three_crows_days)

macd_days = data[data['MACD'] == 0]
#print('MACD :', macd_days)
quote_ctx.close()