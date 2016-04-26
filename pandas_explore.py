import pandas as pd


df = pd.read_csv("Reddit_Whiskey.csv")



def clean_dates(date):
    d = date.split()
    return d[0]

def try_date(date):
    try:
        return pd.to_datetime(date)
    except:
        return pd.to_datetime("2016-01-01")


# Next filter for min number of reviews

# fill in average rating and cost


# filter
#df = df.groupby("Bottle").filter(lambda x: len(x) > 10)

#df[df['A'].str.contains("hello")]






