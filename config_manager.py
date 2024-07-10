import json
import os

CONFIG_FILE = 'pdf_search_config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'last_args': {}, 'favorites': {}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def save_last_args(args):
    config = load_config()
    args_dict = vars(args)
    exclude_args = ['use_previous', 'use_favorite', 'save_favorite']
    config['last_args'] = {k: v for k, v in args_dict.items() if k not in exclude_args and v is not None}
    save_config(config)

def load_args(args, use_previous, use_favorite):
    config = load_config()
    if use_previous:
        loaded_args = config.get('last_args', {})
    elif use_favorite:
        loaded_args = config.get('favorites', {}).get(use_favorite, {})
    else:
        return args

    for key, value in loaded_args.items():
        if getattr(args, key) is None or (isinstance(getattr(args, key), list) and not getattr(args, key)):
            setattr(args, key, value)
    
    return args

def save_favorite(name, args):
    config = load_config()
    args_dict = vars(args)
    exclude_args = ['use_previous', 'use_favorite', 'save_favorite']
    config['favorites'][name] = {k: v for k, v in args_dict.items() if k not in exclude_args and v is not None}
    save_config(config)
    print(f"Saved current arguments as favorite '{name}'")