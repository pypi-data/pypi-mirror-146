from ensurepip import version
from virt import virt, config
import argparse
import os

version = "0.5"

def virtBak():
    configPath = os.path.join(os.environ.get("HOME"), ".virtbak", "virtbak.conf")
    parser = argparse.ArgumentParser(description='Backup virtual machines from LibVirt')
    parser.add_argument('--config', '-c', help='Config file to use', default=configPath)
    parser.add_argument('--machine', '-m', help='Virtual machine to backup')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s ' + version)


    args = parser.parse_args()
    
    conf = config.Config(args.config)


    for con in conf.config:
        if args.machine is not None:
            manager = virt.VirtManager(args.machine)
            if conf.config[con]["dir"] is not None:
                manager.backup(conf.config[con]["dir"])
        else:    
            if conf.config[con] and conf.config[con]["machines"] is not None:
                machines = conf.config[con]["machines"]
                for machine in machines:
                    print("Backing up..." + machine)
                    manager = virt.VirtManager(machine)
                    if conf.config[con]["dir"] is not None:
                        manager.backup(conf.config[con]["dir"])
        
if __name__ == "__main__":
    virtBak()