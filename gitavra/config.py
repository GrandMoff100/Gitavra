import os


def get_config():
    user_base = os.path.expanduser('~')

    try:
        with open(user_base + '/.gitavra') as config:
            lines = config.readlines()
    except FileNotFoundError:
        with open(user_base + '/.gitavra', 'w') as config:
            default_configs = [
                ['LAST_OPENED_REPO', 'None'],
            ]
            config.write('\n'.join(['='.join(config) for config in default_configs]))

        with open(user_base + '/.gitavra') as config:
            lines = config.readlines()

    return {line.split('=')[0]:line.split('=')[1] for line in lines}


def set_config(option, value):
    config = get_config()

    config[option] = value

    lines = ['{}={}'.format(k, v) for k,v in config.items()]

    user_base = os.path.expanduser('~')

    with open(user_base + '/.gitavra', 'w') as config:
        config.writelines(lines)