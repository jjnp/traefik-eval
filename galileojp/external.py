import pandas as pd
import json


def concurrent_req_log_as_df(path):
    df = pd.DataFrame(columns=['timestamp', 'concurrent_clients'])
    with open(path) as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            parsed = json.loads(line)
            df.loc[i] = [parsed['timestamp'], parsed['clients']]
            i += 1
    df['timestamp'] = df['timestamp'].apply(lambda d: pd.to_datetime(d, unit='s'))
    return df


def traefik_weight_log_as_df(path):
    pass