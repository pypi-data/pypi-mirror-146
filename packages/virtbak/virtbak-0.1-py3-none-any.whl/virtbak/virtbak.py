from .virt import virt, config
import argparse
import os

def virtBackup():
    configPath = os.path.join(os.environ.get("HOME"), ".virtbackup", "virtbackup.conf")
    parser = argparse.ArgumentParser(description='Backup virtual machines from LibVirt')
    parser.add_argument('--config', '-c', help='Config file to use', default=configPath)
    parser.add_argument('--server', '-s', help='Server to backup', required=True)


    args = parser.parse_args()

    manager = virt.VirtManager(args.server)
    conf = config.Config(args.config)


    for con in conf.config:
        if  conf.config[con] and conf.config[con]["dir"] is not None:
            manager.backup(conf.config[con]["dir"])