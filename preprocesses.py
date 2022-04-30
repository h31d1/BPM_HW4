import numpy as np 
import pandas as pd

def get_pos_case_length_quantile(data, log_schema, quantile=0.90):
    return int(np.ceil(
        data.groupby(log_schema.get('case_id_col'))\
            .size()\
                .quantile(quantile)))

def split_data_strict(data, log_schema, train_ratio, split="temporal"):  
    """ 
    Split into train and test 
    - Using temporal split 
    - Discard events that overlap the periods
    """
    data = data.sort_values([log_schema.get('timestamp_col'), log_schema.get('activity_col')], ascending=True, kind='mergesort')
    grouped = data.groupby(log_schema.get('case_id_col'))
    start_timestamps = grouped[log_schema.get('timestamp_col')].min().reset_index()
    start_timestamps = start_timestamps.sort_values(log_schema.get('timestamp_col'), ascending=True, kind='mergesort')
    train_ids = list(start_timestamps[log_schema.get('case_id_col')])[:int(train_ratio*len(start_timestamps))]
    train = data[data[log_schema.get('case_id_col')].isin(train_ids)].sort_values([log_schema.get('timestamp_col'), log_schema.get('activity_col')], ascending=True, kind='mergesort')
    test = data[~data[log_schema.get('case_id_col')].isin(train_ids)].sort_values([log_schema.get('timestamp_col'), log_schema.get('activity_col')], ascending=True, kind='mergesort')
    split_ts = test[log_schema.get('timestamp_col')].min()
    train = train[train[log_schema.get('timestamp_col')] < split_ts]
    return (train, test)

def generate_prefix_data(data, log_schema, min_length, max_length, gap=1):
    # generate prefix data (each possible prefix becomes a trace)
    data['case_length'] = data.groupby(log_schema.get('case_id_col'))[log_schema.get('activity_col')].transform(len)

    dt_prefixes = data[data['case_length'] >= min_length].groupby(log_schema.get('case_id_col')).head(min_length)
    dt_prefixes["prefix_nr"] = 1
    dt_prefixes["orig_case_id"] = dt_prefixes[log_schema.get('case_id_col')]
    for nr_events in range(min_length+gap, max_length+1, gap):
        tmp = data[data['case_length'] >= nr_events].groupby(log_schema.get('case_id_col')).head(nr_events)
        tmp["orig_case_id"] = tmp[log_schema.get('case_id_col')]
        tmp[log_schema.get('case_id_col')] = tmp[log_schema.get('case_id_col')].apply(lambda x: "%s_%s"%(x, nr_events))
        tmp["prefix_nr"] = nr_events
        dt_prefixes = pd.concat([dt_prefixes, tmp], axis=0)

    dt_prefixes['case_length'] = dt_prefixes['case_length'].apply(lambda x: min(max_length, x))

    return dt_prefixes