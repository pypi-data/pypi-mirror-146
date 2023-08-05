from asyncore import write
import libvirt
import sys
from lxml import etree
from argparse import ArgumentParser
from typing import Any
import os
from datetime import datetime

class VirtManager:
    server = ""
    dom0 = None
    connection = None
    devices = []
    disks = []
    xml = None
    
    def __init__(self, server):
        self.server = server
        try:
            self.connection = libvirt.openReadOnly(None)
        except libvirt.libvirtError:
            print('Failed to open connection to the hypervisor')
            sys.exit(1)

        try:
            self.dom0 = self.connection.lookupByName(self.server)
        except libvirt.libvirtError:
            print('Failed to find the main domain')
            sys.exit(1)
            
        self.set_devices_from_xml()
        self.disks = self.find_disks()
        self.xml = self.dom0.XMLDesc()
        
    
    def find_device(self, ctx, path: str):
        res = ctx.xpath(path)
        if res is None or len(res) == 0:
            value = "Unknown"
        else:
            value = res[0]
        return value
    
    def find_disks(self):
        disk_list = []
        for dev in self.devices:
            if dev["Type"] == "file" and dev["Device"] == "disk":
                
                disk_list.append({
                    "Path": os.path.dirname(os.path.abspath(dev["Source"])),
                    "File": os.path.basename(dev["Source"]),
                    "Full": dev["Source"],
                })
        return disk_list
    
    def set_devices_from_xml(self):
        #doc = libxml2.parseDoc(self.dom0.XMLDesc())
        doc = etree.fromstring(self.dom0.XMLDesc())
        devs = doc.xpath("/domain/devices/*")
        for d in devs:            
            type = self.find_device(d, "@type")
            if type == "file":
                self.devices.append({
                    "Type": type,
                    "Source": self.find_device(d, "source/@file"),
                    "Target": self.find_device(d, "target/@dev"),
                    "Device": self.find_device(d, "@device"),
                })
            elif type == "block":
                self.devices.append({
                    "Type": type,
                    "Source": self.find_device(d, "source/@file"),
                    "Target": self.find_device(d, "target/@dev"),
                })
            elif type == "bridge":
                self.devices.append({
                    "Type": type,
                    "Source": self.find_device(d, "source/@file"),
                    "MAC": self.find_device(d, "mac/@address"),
                    "Model": self.find_device(d, "model/@type"),
                })
            elif type == "network":
                self.devices.append({
                    "Type": type,
                    "MAC": self.find_device(d, "mac/@address"),
                    "Model": self.find_device(d, "model/@type"),
                })
            elif type == "usb":
                self.devices.append({
                    "Type": type,
                    "Slot": self.find_device(d, "address/@slot"),
                    "Model": self.find_device(d, "@model")
                })
            elif type == "pci":
                self.devices.append({
                    "Type": type,
                    "Slot": self.find_device(d, "address/@slot"),
                    "Model": self.find_device(d, "@model")
                })
            elif type == "ide":
                self.devices.append({
                    "Type": type,
                    "Slot": self.find_device(d, "address/@slot"),
                    "Model": self.find_device(d, "@model")
                })
            elif type == "video":
                self.devices.append({
                    "Type": type,
                    "Model": self.find_device(d, "model/@type"),
                    "Ram": self.find_device(d, "model/@ram"),
                    "Vram": self.find_device(d, "model/@vram"),
                    "VGAmem": self.find_device(d, "model/@vgamem"),
                    "Slot": self.find_device(d, "address/@slot"),
                })
                
            
        
        return self
    
    def restore_script(self):
        restore = '''#!/bin/env bash
echo Copying files...
{}
echo Creating domain...
virsh create {}
'''
        
        copy = '''cp -av {} {}'''
        
        copyStr = ""
        
        for disks in self.disks:
            copyStr = copy.format(disks["File"], disks["Path"]) + copyStr
            
        return restore.format(copyStr, self.server+".xml")
        
    def make_executable(self, path):
        mode = os.stat(path).st_mode
        mode |= (mode & 0o444) >> 2    # copy R bits to X
        os.chmod(path, mode)
        
        
    def backup(self, dir="."):
        nowDateTime = datetime.now().strftime("%Y%m%d_%H%M")
        fullPath = os.path.join(dir, self.server)
        xmlPath = os.path.join(fullPath, self.server + ".xml")
        restoreScriptPath = os.path.join(fullPath, "restore.sh")
        tarFileName = self.server + "_" + nowDateTime + ".tar.gz"
        tarFilePath = os.path.join(dir, tarFileName)
        
        
        if not os.path.exists(fullPath):
            print("Creating backup folder... ")
            os.makedirs(fullPath)
            os.chmod( fullPath, 0o777)
        
        print("Dumping... " + self.server)
        os.system("virsh dumpxml {} > {}".format(self.server, xmlPath))
        
        print("Creating restore script... ")
        with open(restoreScriptPath, "w") as f:
            f.write(self.restore_script())
        self.make_executable(restoreScriptPath)
        
        for disk in self.disks:
            print("Backing up {}".format(disk["Full"]))
            os.system("rsync -avP {} {}".format(self.disks[0]["Full"], fullPath))
        
        os.system("chmod -R 0777 {}".format(fullPath))
        
        print("Creating archive...")
        os.system("tar -cvzf {} {}".format(fullPath, tarFilePath))
        
        print("Cleanin up...")
        os.system("rm -rf {}".format(fullPath))  
        
        print("Backup complete!")
            
            
        