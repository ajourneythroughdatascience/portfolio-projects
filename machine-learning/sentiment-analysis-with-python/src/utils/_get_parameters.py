# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:29:01 2023

@author: Pablo Aguirre

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# Third-party packages
import tomli

# Main class
class GetParameters:
    '''
    Mixin class:
        - Get parameters
        - Get configuration
    '''
    def getConfig(self):
        '''
        Get configuration from .toml file
        '''
        with open("config/config.toml", mode="rb") as f_conf:
            config = tomli.load(f_conf)

        return config

    def getParams(self):
        '''
        Get parameters from .toml file
        '''
        with open("config/parameters.toml", mode="rb") as f_params:
            params = tomli.load(f_params)

        return params

if __name__ == '__main__':
    main() # type: ignore