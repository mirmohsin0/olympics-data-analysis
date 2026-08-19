import pandas as pd 


def preprocess(df, region):

    # filtering the summer olympics 
    df = df[df['Season'] == 'Summer']

    #merge with region 
    df = df.merge(region, on='NOC', how='left')

    #dropping duplicates 
    df.drop_duplicates(inplace=True)

    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df