import baostock as bs
import pandas as pd

code_num = 'sz.002039'
start_date = '2016-01-01'
end_date = '2023-12-12'
frequency = 'w'
res_path = rf'C:\Users\18085\Desktop\{code_num}.csv'

lg = bs.login()
print('login respond error_code:'+lg.error_code)
print('login respond error_msg:'+lg.error_msg)

rs = bs.query_history_k_data_plus(code_num,
    #"date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
    start_date, end_date,
    frequency, adjustflag="3")

print('query_history_k_data respond error_code:'+rs.error_code)
print('query_history_k_data respond  error_msg:'+rs.error_msg)
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
result.to_csv(res_path, encoding="utf-8", index=False)######修改存放数据的地方
bs.logout()