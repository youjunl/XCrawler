import pandas as pd

enginstr = "mysql+pymysql://admin:Sybz452731@192.168.200.118:3306/xcrawler"
def queryData(table,selectName,time):
    try:
        data_table = pd.read_sql_table(table, enginstr)
    except:
        data_table = None
    if data_table is not None:
       sql = f"SELECT * FROM {table} WHERE {selectName} = '{time}'"
       df = pd.read_sql(sql, enginstr)
       print(df)
       
# queryData("stock","日期","2023-11-29")