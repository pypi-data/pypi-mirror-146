import pandas as pd
from regbot import signal

df = pd.read_csv('../../../jupyter/regbot_v4.csv')
#df = pd.read_csv('../../../crypto/freqtrade/sell.csv')
print(df.columns)
y_pred = []
def getSignal(open,close):
    return signal(open,close)


df = df[df['buy'] == 0]
print(df.head())

df['result'] = df.apply(lambda row: getSignal(row['open'], row['close']), axis=1)

print(df.head())

print(len(df[df['result'] == df['buy']]), len(df))
