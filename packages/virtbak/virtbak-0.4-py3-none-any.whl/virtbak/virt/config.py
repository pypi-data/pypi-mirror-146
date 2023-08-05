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
            dirGet = self.parser.get(section, "dir")
            self.config[section] = { "dir": dirGet }
        
