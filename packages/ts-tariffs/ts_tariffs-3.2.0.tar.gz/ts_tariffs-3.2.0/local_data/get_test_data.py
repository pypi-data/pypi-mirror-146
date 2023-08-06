import pandas as pd


data_details = {
    'load': {
        'url': 'https://open-energy-data.s3.ap-southeast-2.amazonaws.com/load_data.csv',
        'dt_format': '%Y-%m-%d %H:%M:%S%z',
        'datetime_col': 'Datetime'
    },
    'solar': {
        'url': 'https://open-energy-data.s3.ap-southeast-2.amazonaws.com//solar_data.csv',
        'dt_format': '%Y-%m-%d %H:%M:%S%z',
        'datetime_col': 'Datetime'
    },
    'wholesale': {
        'url': 'https://open-energy-data.s3.ap-southeast-2.amazonaws.com/wholesale_data.csv',
        'dt_format': '%Y-%m-%d %H:%M:%S%z',
        'datetime_col': 'Datetime'
    }
}


def get_data(data_name) -> pd.DataFrame:
    data = pd.read_csv(data_details[data_name]['url'])
    data.index = pd.to_datetime(
        data[data_details[data_name]['datetime_col']],
        format=data_details[data_name]['dt_format'],
        utc=False
    )
    data.index = data.index.map(lambda t: t.replace(tzinfo=None))
    return data
