from dv_elt_lib.gp_utils import select_df_generator
from dv_elt_lib.ch_ulits import insert_df


def gp_ch_copy(gp_conn, ch_client, src_path, dst_path, batch_size=1_000_000):
    select_query = f"select * from {src_path}"
    for df in select_df_generator(gp_conn, select_query, batch_size=batch_size):
        insert_df(df, ch_client, dst_path)