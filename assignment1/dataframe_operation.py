def add_avg(df):
    df=df.append(dff.mean(),ignore_index=True)
    df.iloc[-1,0]='avg'
    return df
