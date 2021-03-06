try:
    from configparser import ConfigParser
    from os.path import dirname, abspath, exists
    from os import makedirs
except ImportError as e:
    print("Import Error in config.py:",e)

# Location of config.ini
config_location = dirname(dirname(abspath(__file__))) + "/config.ini",

# Normal settings should go in config.ini, but you can change the
#   default settings below if you'd rather. Make sure the types in conf and conf_type match.
#   config.ini is unnecessary if you'd rather use the settings here instead.
# Setting names must match in conf, conf_type, and in config.ini.

conf = {
    "ckey" : '',
    "csecret" : '',
    "atoken" : '',
    "asecret" : '',
    "appid" : '',
    "appkey" : '',
    "verbose" : False,
    "export_dir" : dirname(dirname(abspath(__file__))) + '/output/',
    "startup_connect" : True,
    "mongo_timeout" : 30,
    "tweet_similarity_threshold" : .6,
    "tweet_duplicate_limit" : 10,
}

empty = ["ckey","csecret","atoken","asecret","appid","appkey"] # Settings that can be empty
paths = ["export_dir"]

conf_type = {
    "ckey" : str,
    "csecret" : str,
    "atoken" : str,
    "asecret" : str,
    "appid" : str,
    "appkey" : str,
    "verbose" : bool,
    "export_dir" : str,
    "startup_connect" : bool,
    "mongo_timeout" : int,
    "tweet_similarity_threshold" : float,
    "tweet_duplicate_limit" : int,
}

def verify_path(path):
    try:
        path = abspath(path) + "/"
        # print(path)
        if not exists(path):
            makedirs(path)
        return path
    except Exception as e:
        print("Error in config.py:",e)
        return None

def cast_type(key, val):
    # Use the key to get the required type and its current type
    req_type = conf_type[key]
    if type(val) is req_type:
        return val
    try:
        # Type cast the value. "mongo_timeout" : int
        #   so, c_val = int(val)
        # Remember that bools typecast differently: bool(3) = True
        #   or bool('False') = True ('False', being a string)
        if req_type is bool:
            if val.lower() in ['false', '0', 'no','disabled']:
                return False
            elif val.lower() in ['true','1','yes','enabled']:
                return True
        c_val = req_type(val)
        return c_val
    except ValueError:
        return None

def read_conf():
    # Loop through values in config.ini
    config = ConfigParser()
    config.read(config_location)
    for section in config.sections():
        for key in config[section]:
            if key in conf:
                try:
                    value = config[section][key].strip()
                    val = cast_type(key, value)
                    if  value == "DEFAULT":
                        if key in paths:
                            verify_path(conf[key])
                        continue
                    elif key in paths:
                        val = verify_path(val)
                    elif (val is None or (type(val) is str and not len(val))) and key not in empty:
                        print(key,"=",config[section][key], "in config is invalid, using default value.")
                        continue
                    conf[key] = val
                except Exception as e:
                    print("Error in config.py:",e)
                    continue

# Initial load
read_conf()

if not exists(*config_location):
    print("config.ini not found! Using default values.")
    for path in paths:
        conf[path] = verify_path(conf[path])
