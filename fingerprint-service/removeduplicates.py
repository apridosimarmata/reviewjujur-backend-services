import pandas as pd

df = pd.read_csv('ordered_fingerprints.csv')
df.drop_duplicates(inplace=True)
df.to_csv('ordered_fingerprints.csv', index=False)