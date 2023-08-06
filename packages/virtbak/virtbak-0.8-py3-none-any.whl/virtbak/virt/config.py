import configparser
import os
from configparser import ConfigParser

class Config:
    filename = os.path.join(os.environ.get("HOME"), ".virtbackup", "virtbackup.conf")
    parser = ConfigParser()
    config = {}
    
    
    def __init__(self, filename=None) -> None:
        if filename is not None:
            self.filename = filename
        
        self.parser.read(self.filename)
        
        for section in self.parser.sections():
            optionList = {}
            for option in self.parser.options(section):
                
                try:
                    value=self.parser.getint(section,option)
                except ValueError:
                    if option == "dir":
                        value = self.parser.get(section,option)
                    else:
                        value=self.parser.get(section,option).split(',')
                optionList[option] = value

            self.config[section] = optionList
        
