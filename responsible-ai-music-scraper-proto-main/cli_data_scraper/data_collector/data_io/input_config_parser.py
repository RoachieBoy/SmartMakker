from data_collector.data_io.run_configuration import RunConfiguration

import json


def load_parse_input_config(config_filepath: str) -> RunConfiguration:
    """
    Convert json config file to run configuration

    :param config_filepath: Filepath to config file
    :return: Run configuration
    """

    parsed_config = json.load(open(config_filepath, 'r'))

    configs = RunConfiguration({})

    for backend_id in parsed_config.keys():
        backend_name = parsed_config[backend_id]['name']
        args = parsed_config[backend_id]['call_arguments']

        name_args_tuple = (backend_name, json.dumps(args))

        configs.backend_arguments[backend_id] = name_args_tuple

    return configs
