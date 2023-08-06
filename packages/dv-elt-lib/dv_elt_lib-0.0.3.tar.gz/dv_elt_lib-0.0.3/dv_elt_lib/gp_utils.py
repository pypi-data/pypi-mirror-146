import logging

import pandas as pd


def _insert_batch_df(df, conn, table, log=logging.getLogger(__name__)):
    """
    Insert pandas dataframe to table
    :param df: dataframe to insert
    :param conn: pg/gp connection
    :param table: target table name
    :return:
    """
    cursor = conn.cursor()
    cols = df.columns.tolist()
    values = [cursor.mogrify("(%s)" % ','.join('%s' for _ in cols), tup).decode('utf8') for tup in
              df.itertuples(index=False)]
    query = "INSERT INTO %s(%s) VALUES " % (table, ','.join(cols)) + ",".join(values)
    cursor.execute(query)
    conn.commit()
    cursor.close()


def insert_df(df, conn, table, batch_size=1_000_000, log=logging.getLogger(__name__)):
    """
    Insert data from pandas dataframe into table in batch mode'
    :param df: dataframe to insert
    :param conn: pg/gp connection
    :param table: target table name
    :param batch_size: batch size
    :return:
    """
    size = df.shape[0]
    for ind in range(0, size, batch_size):
        _insert_batch_df(df.iloc[ind:ind + batch_size], conn, table, log=log)
        log.info(f"batch of size {min(batch_size, size-ind)} was inserted")


def select_df(conn, query, batch_size=1_000_000, log=logging.getLogger(__name__)):
    cur = conn.cursor()
    cur.execute(f"DECLARE cursor CURSOR FOR ({query});")

    def fetch_df(cur):
        cur.execute(f"""FETCH FORWARD {batch_size} FROM cursor;""")
        rows = cur.fetchall()
        log.info(f"batch of size {len(rows)} was selected")
        columns = [desc[0] for desc in cur.description]
        return pd.DataFrame(rows, columns=columns)
    dfs = []
    _df = fetch_df(cur)
    while _df.shape[0] != 0:
        dfs.append(_df)
        _df = fetch_df(cur)
    return pd.concat(dfs, axis=0)


def select_df_generator(conn, query, batch_size=1_000_000, log=logging.getLogger(__name__)):
    cur = conn.cursor()
    cur.execute(f"DECLARE cursor CURSOR FOR ({query});")

    def fetch_df(cur):
        cur.execute(f"""FETCH FORWARD {batch_size} FROM cursor;""")
        rows = cur.fetchall()
        log.info(f"batch of size {len(rows)} was selected")
        columns = [desc[0] for desc in cur.description]
        return pd.DataFrame(rows, columns=columns)
    _df = fetch_df(cur)
    while _df.shape[0] != 0:
        yield _df
        _df = fetch_df(cur)
