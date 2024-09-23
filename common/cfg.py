#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from .oslocfgbase import CONF
import configparser
from manage import *


class Config():

    def __init__(self):
        pass

    def get(self, key):
        return self.__dict__.get(key, None)

    def set(self, key, value):
        self.__dict__[key] = value
        return self.__dict__[key]



def parseCfg(cfgPath):
    # config file parse
    CONF(default_config_files=[cfgPath])
    SETTINGS["default"]["wiresharkPath"] = CONF.default.wiresharkPath
    for host in CONF.linux.host:
        SETTINGS["linux"]["host"].append(host.replace("\\\n", ''))
    for port in CONF.linux.port:
        SETTINGS["linux"]["port"].append(port.replace("\\\n", ''))
    for user in CONF.linux.user:
        SETTINGS["linux"]["user"].append(user.replace("\\\n", ''))
    for password in CONF.linux.password:
        SETTINGS["linux"]["password"].append(password.replace("\\\n", ''))
    for su_user in CONF.linux.su_user:
        SETTINGS["linux"]["su_user"].append(su_user.replace("\\\n", ''))
    for su_password in CONF.linux.su_password:
        SETTINGS["linux"]["su_password"].append(su_password.replace("\\\n", ''))
    for cmd in CONF.linux.cmd:
        SETTINGS["linux"]["cmd"].append(cmd.replace("\\\n", ''))

    for host in CONF.esxi.host:
        SETTINGS["esxi"]["host"].append(host.replace("\\\n", ''))
    for port in CONF.esxi.port:
        SETTINGS["esxi"]["port"].append(port.replace("\\\n", ''))
    for user in CONF.esxi.user:
        SETTINGS["esxi"]["user"].append(user.replace("\\\n", ''))
    for password in CONF.esxi.password:
        SETTINGS["esxi"]["password"].append(password.replace("\\\n", ''))
    for cmd in CONF.esxi.cmd:
        SETTINGS["esxi"]["cmd"].append(cmd.replace("\\\n", ''))

def writeCfg(cfgPath):
    # config file parse
    CONF(default_config_files=[cfgPath])

def parseConfig(cfgPath):
    # config = configparser.ConfigParser()
    config = configparser.RawConfigParser()
    config.read(cfgPath)
    sections = config.sections()

    SETTINGS["default"]["wiresharkPath"] = config["default"]["wiresharkPath"]
    tmp = config["linux"]["host"].split(',')
    tmp.insert(0, "")
    for host in tmp:
        SETTINGS["linux"]["host"].append(host.replace("\\\n", ''))
    tmp = config["linux"]["port"].split(',')
    tmp.insert(0, "")
    for port in tmp:
        SETTINGS["linux"]["port"].append(port.replace("\\\n", ''))
    tmp = config["linux"]["user"].split(',')
    tmp.insert(0, "")
    for user in tmp:
        SETTINGS["linux"]["user"].append(user.replace("\\\n", ''))
    tmp = config["linux"]["password"].split(',')
    tmp.insert(0, "")
    for password in tmp:
        SETTINGS["linux"]["password"].append(password.replace("\\\n", ''))
    tmp = config["linux"]["su_user"].split(',')
    tmp.insert(0, "")
    for su_user in tmp:
        SETTINGS["linux"]["su_user"].append(su_user.replace("\\\n", ''))
    tmp = config["linux"]["su_password"].split(',')
    tmp.insert(0, "")
    for su_password in tmp:
        SETTINGS["linux"]["su_password"].append(su_password.replace("\\\n", ''))
    tmp = config["linux"]["cmd"].split(',')
    tmp.insert(0, "")
    for cmd in tmp:
        SETTINGS["linux"]["cmd"].append(cmd.replace("\\\n", ''))

    tmp = config["esxi"]["host"].split(',')
    tmp.insert(0, "")
    for host in tmp:
        SETTINGS["esxi"]["host"].append(host.replace("\\\n", ''))
    tmp = config["esxi"]["port"].split(',')
    tmp.insert(0, "")
    for port in tmp:
        SETTINGS["esxi"]["port"].append(port.replace("\\\n", ''))
    tmp = config["esxi"]["user"].split(',')
    tmp.insert(0, "")
    for user in tmp:
        SETTINGS["esxi"]["user"].append(user.replace("\\\n", ''))
    tmp = config["esxi"]["password"].split(',')
    tmp.insert(0, "")
    for password in tmp:
        SETTINGS["esxi"]["password"].append(password.replace("\\\n", ''))
    tmp = config["esxi"]["cmd"].split(',')
    tmp.insert(0, "")
    for cmd in tmp:
        SETTINGS["esxi"]["cmd"].append(cmd.replace("\\\n", ''))

def writeConfig(cfgPath):
    # config = configparser.ConfigParser()
    config = configparser.RawConfigParser()
    config.read(cfgPath)
    sections = config.sections()
    SETTINGS["linux"]["host"].remove("")
    tmp = config["linux"]["host"].split(',')
    for host in tmp:
        SETTINGS["linux"]["host"].append(host.replace("\\\n", ''))
    tmp = config["linux"]["port"].split(',')
    for port in tmp:
        SETTINGS["linux"]["port"].append(port.replace("\\\n", ''))
    tmp = config["linux"]["user"].split(',')
    for user in tmp:
        SETTINGS["linux"]["user"].append(user.replace("\\\n", ''))
    tmp = config["linux"]["password"].split(',')
    for password in tmp:
        SETTINGS["linux"]["password"].append(password.replace("\\\n", ''))
    tmp = config["linux"]["su_user"].split(',')
    for su_user in tmp:
        SETTINGS["linux"]["su_user"].append(su_user.replace("\\\n", ''))
    tmp = config["linux"]["su_password"].split(',')
    for su_password in tmp:
        SETTINGS["linux"]["su_password"].append(su_password.replace("\\\n", ''))
    tmp = config["linux"]["cmd"].split(',')
    for cmd in config["linux"]["cmd"]:
        SETTINGS["linux"]["cmd"].append(cmd.replace("\\\n", ''))

    tmp = config["esxi"]["host"].split(',')
    for host in tmp:
        SETTINGS["esxi"]["host"].append(host.replace("\\\n", ''))
    tmp = config["esxi"]["port"].split(',')
    for port in config["esxi"]["port"]:
        SETTINGS["esxi"]["port"].append(port.replace("\\\n", ''))
    tmp = config["esxi"]["user"].split(',')
    for user in config["esxi"]["user"]:
        SETTINGS["esxi"]["user"].append(user.replace("\\\n", ''))
    tmp = config["esxi"]["password"].split(',')
    for password in config["esxi"]["password"]:
        SETTINGS["esxi"]["password"].append(password.replace("\\\n", ''))
    tmp = config["esxi"]["cmd"].split(',')
    for cmd in config["esxi"]["cmd"]:
        SETTINGS["esxi"]["cmd"].append(cmd.replace("\\\n", ''))

