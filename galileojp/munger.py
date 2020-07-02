import numpy as np
import pandas as pd


def to_metric_table_series(telem, node, window='1s'):
    """
    Transforms the long-format telemetry timeseries into a wide-timeseries by resampling in a window and creating
    columns for each metric.

    :param telem: the telemetry data frame returned by ExperimentFrameGateway.telemetry()
    :param node: the node to filter
    :param window: the window size for resampling (default = 1s)
    :return: a new dataframe
    """
    df = telem[telem['NODE'] == node][['METRIC', 'VALUE']]

    ts_cpu = df[df['METRIC'] == 'cpu']
    ts_cpu = pd.Series(data=np.asarray(ts_cpu['VALUE']), index=ts_cpu.index)
    ts_cpu = ts_cpu.resample(window).mean()

    ts_freq = df[df['METRIC'] == 'freq']
    ts_freq = pd.Series(data=np.asarray(ts_freq['VALUE']), index=ts_freq.index)
    ts_freq = ts_freq.resample(window).mean()

    ts_rx = df[df['METRIC'] == 'rx']
    ts_rx = pd.Series(data=np.asarray(ts_rx['VALUE']), index=ts_rx.index)
    ts_rx = ts_rx.resample(window).mean()

    ts_tx = df[df['METRIC'] == 'tx']
    ts_tx = pd.Series(data=np.asarray(ts_tx['VALUE']), index=ts_tx.index)
    ts_tx = ts_tx.resample(window).mean()

    ts_rd = df[df['METRIC'] == 'rd']
    ts_rd = pd.Series(data=np.asarray(ts_rd['VALUE']), index=ts_rd.index)
    ts_rd = ts_rd.resample(window).mean()

    ts_wr = df[df['METRIC'] == 'wr']
    ts_wr = pd.Series(data=np.asarray(ts_wr['VALUE']), index=ts_wr.index)
    ts_wr = ts_wr.resample(window).mean()

    ts_watt = df[df['METRIC'] == 'watt']
    ts_watt = pd.Series(data=np.asarray(ts_watt['VALUE']), index=ts_watt.index)
    ts_watt = ts_watt.resample(window).mean()

    return pd.DataFrame({
        'cpu': ts_cpu,
        'freq': ts_freq,
        'rx': ts_rx,
        'tx': ts_tx,
        'rd': ts_rd,
        'wr': ts_wr,
        'watt': ts_watt}, index=ts_cpu.index)
