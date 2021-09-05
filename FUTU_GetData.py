from futu import *
import futu as ft
import pandas as pd

quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111, is_encrypt=False) #OK!! 2021.09.01 12:55am
start_dt = datetime.today()-timedelta(365)
end_dt = datetime.today()
print("Start: " + start_dt.strftime("%Y-%m-%d"))
print("End: " + end_dt.strftime("%Y-%m-%d"))
start_dt_str = start_dt.strftime("%Y-%m-%d")
end_dt_str = end_dt.strftime("%Y-%m-%d")
print(quote_ctx.get_market_snapshot(['HK.00700','HK.00388']))

ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start=start_dt_str, end=end_dt_str, max_count=999999)
if ret == RET_OK:
    print(data)
    print(data['code'][0])    # 取第一条的股票代码
    print(data['close'].values.tolist())   # 第一页收盘价转为 list
else:
    print('error:', data)

print('=========================================')
ret, data = quote_ctx.get_capital_flow("HK.00700")
if ret == RET_OK:
    print(data)
    print(data['in_flow'][0]) # Take the first net inflow of capital
    print(data['in_flow'].values.tolist()) # Convert to list
    data.to_csv('fdata.csv') #Save Dataframe to .CSV
else:
    print('error:', data)

print('=========================================')
accumulate_filter = AccumulateFilter()
accumulate_filter.stock_field = StockField.AMPLITUDE
accumulate_filter.filter_min = 30
accumulate_filter.filter_max = 40
accumulate_filter.is_no_filter = False
accumulate_filter.sort = SortDir.ASCEND
ret, ls = quote_ctx.get_stock_filter(Market.HK, [accumulate_filter])
Our_stock_list = []
if ret == RET_OK:
    last_page, all_count, stock_list = ls
    print(len(stock_list), stock_list)
    for item in stock_list:
        Our_stock_list.append(item.stock_code)
        print(item.stock_code, item.stock_name)
    print(Our_stock_list)
else:
    print('error:', ls)

print('=========================================')
ret, data = quote_ctx.get_plate_list(Market.HK, Plate.CONCEPT)
if ret == RET_OK:
    print(data)
    print(data['plate_name'][0]) # Take the first plate name
    print(data['plate_name'].values.tolist()) # Convert to list
    data.to_csv('get_plate_list.csv')  # Save Dataframe to .CSV
    data_plate_list = []
    for i in data.code:
        data_plate_list.append(i)
    print('data_plate_list: ', data_plate_list)
else:
    print('error:', data)

quote_ctx.close()