import json
import argparse

from .config_manager import *

import re

def namedModulePair(value):
    matches = (re.match(r"^(([^\s:]+)?:)?([^\s:]+)(:(\S+)?)?$", value))
    if matches is None:
        raise argparse.ArgumentTypeError
    
    name = (matches.group(2))
    moduleName = (matches.group(3))
    configClassName = (matches.group(5))



    return name,moduleName, configClassName


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate a config file that combines content inside the Config class in each module specified.")

    parser.add_argument("entry", nargs="*" , type = namedModulePair, help = """pair of [[name]:]moduleName[:[configClassName]], 
                                                                            if name is not specified, by default it will use the moduleName.
                                                                            If configClassName is not specified, it will look for the class Config under the module""")
    parser.add_argument("--outputFilename")

    args = parser.parse_args()

    config = dict()



    for name, moduleName,configClassName in args.entry:
        if name is None:
            name = moduleName
        if configClassName is None:
            configClassName = "Config"



        configEntry= makeModuleConf(moduleName, configClassName)


        config[name] = toDict(configEntry)


    configText = json.dumps(config, indent='\t')

    if args.outputFilename is None:
        print(configText)
    else:
        with open(args.outputFilename, 'w') as f:
            f.write(configText)

