import pandas as pd
CSV = "SERVER_TEST_NULL_10_100_1000.csv"
df = pd.read_csv(CSV)  
plot =  df.groupby(["STATUS_CODE"]).sum().plot(kind='pie',y='STATUS_CODE')