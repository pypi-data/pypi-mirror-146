

def insert_df(df, ch_client, dst_path, batch_size=1_000_000):
    for i in range(0, df.shape[0], batch_size):
        ch_client.insert_dataframe(f"insert into {dst_path} values", df.iloc[i: i+batch_size])


def select_df(ch_client, query):
    return ch_client.query_dataframe(query)