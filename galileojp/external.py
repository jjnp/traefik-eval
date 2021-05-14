import pandas as pd
import json
from datetime import datetime


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


def traefik_weight_log_as_df(path, service_name='pdf', only_full_rows=True):
    # hosts = _find_hosts(path, service_name)
    msg = 'updating weights'
    with open(path) as f:
        lines = f.readlines()
        # df = pd.DataFrame()
        rows = []
        for line in lines:
            parsed = json.loads(line)
            if parsed['msg'] == msg and parsed['serviceName'] == service_name:
                row = {}
                row['timestamp'] = datetime.strptime(parsed['time'],'%Y-%m-%dT%H:%M:%SZ')
                weights = parsed['weights']
                # print(weights)
                # print(type(weights))
                for h, w in weights.items():
                    row[h] = w
                rows.append(row)
        df = pd.DataFrame(rows).dropna()
        df = df.set_index('timestamp')
        df.reset_index()
        return df

