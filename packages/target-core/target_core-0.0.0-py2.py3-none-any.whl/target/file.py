import gzip
import lzma
import json

# Package imports
from target.logger import get_logger

LOGGER = get_logger()


def config_file(config_path, datetime_format={
        'timestamp_format': '%Y%m%dT%H%M%S',
        'date_format': '%Y%m%d'}):

    naming_convention_default = '{stream}-{timestamp}.json' \
        .replace('{timestamp}', '{timestamp:' + datetime_format['timestamp_format'] + '}') \
        .replace('{date}', '{date:' + datetime_format['date_format'] + '}')

    config = {
        'naming_convention': naming_convention_default,
        'memory_buffer': 64e6
    }

    with open(config_path) as input_file:
        config.update(json.load(input_file))

    config['naming_convention_default'] = naming_convention_default
    config['naming_convention'] = config['naming_convention'] \
        .replace('{timestamp}', '{timestamp:' + datetime_format['timestamp_format'] + '}') \
        .replace('{date}', '{date:' + datetime_format['date_format'] + '}')

    return config


def config_compression(config_default):
    config = {
        'compression': 'none'
    }
    config.update(config_default)

    if f"{config.get('compression')}".lower() == 'gzip':
        config['open_func'] = gzip.open
        config['naming_convention_default'] = config['naming_convention_default'] + '.gz'
        config['naming_convention'] = config['naming_convention'] + '.gz'

    elif f"{config.get('compression')}".lower() == 'lzma':
        config['open_func'] = lzma.open
        config['naming_convention_default'] = config['naming_convention_default'] + '.xz'
        config['naming_convention'] = config['naming_convention'] + '.xz'

    elif f"{config.get('compression')}".lower() in {'', 'none'}:
        config['open_func'] = open

    else:
        raise NotImplementedError(
            "Compression type '{}' is not supported. "
            "Expected: 'none', 'gzip', or 'lzma'"
            .format(f"{config.get('compression')}".lower()))

    return config


def save_jsonl_file(file_data, config):
    if any(file_data['file_data']):
        with config.get('open_func')(file_data['file_name'], 'at', encoding='utf-8') as output_file:
            output_file.writelines((json.dumps(record) + '\n' for record in file_data['file_data']))

        del file_data['file_data'][:]
        LOGGER.debug("'{}' file saved using open_func '{}'".format(file_data['file_name'], config.get('open_func').__name__))
