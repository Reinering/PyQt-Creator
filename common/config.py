#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import os, threading
import configparser
from copy import deepcopy

class Config():
    _instance_lock = threading.Lock()

    # 支持多线程
    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def get(self, key):
        return self.__dict__.get(key, None)

    def set(self, key, value):
        self.__dict__[key] = value
        return self.__dict__[key]

    def setFile(self, configPath):
        self.configPath = configPath
        try:
            # self.cfg = configparser.ConfigParser()
            self.cfg = configparser.RawConfigParser()
        except Exception as e:
            print(e)
        self.cfg.read(configPath)

    def read(self, settings):
        settings["default"]["wiresharkPath"] = self.cfg["default"]["wiresharkPath"]

        tmp = self.cfg["linux"]["host"].split(',')
        # if tmp[0] != '':
        #     tmp.insert(0, "")
        for host in tmp:
            host = host.lstrip()
            settings["linux"]["host"].append(host.replace("\\\n", ''))
        tmp = self.cfg["linux"]["port"].split(',')
        for port in tmp:
            port = port.lstrip()
            settings["linux"]["port"].append(port.replace("\\\n", ''))
        tmp = self.cfg["linux"]["user"].split(',')
        for user in tmp:
            user = user.lstrip()
            settings["linux"]["user"].append(user.replace("\\\n", ''))
        tmp = self.cfg["linux"]["password"].split(',')
        for password in tmp:
            password = password.lstrip()
            settings["linux"]["password"].append(password.replace("\\\n", ''))
        tmp = self.cfg["linux"]["su_user"].split(',')
        for su_user in tmp:
            su_user = su_user.lstrip()
            settings["linux"]["su_user"].append(su_user.replace("\\\n", ''))
        tmp = self.cfg["linux"]["su_password"].split(',')
        for su_password in tmp:
            su_password = su_password.lstrip()
            settings["linux"]["su_password"].append(su_password.replace("\\\n", ''))
        tmp = self.cfg["linux"]["cmd"].split(',')
        for cmd in tmp:
            cmd = cmd.lstrip()
            settings["linux"]["cmd"].append(cmd.replace("\\\n", ''))

        tmp = self.cfg["esxi"]["host"].split(',')
        for host in tmp:
            host = host.lstrip()
            settings["esxi"]["host"].append(host.replace("\\\n", ''))
        tmp = self.cfg["esxi"]["port"].split(',')
        for port in tmp:
            port = port.lstrip()
            settings["esxi"]["port"].append(port.replace("\\\n", ''))
        tmp = self.cfg["esxi"]["user"].split(',')
        for user in tmp:
            user = user.lstrip()
            settings["esxi"]["user"].append(user.replace("\\\n", ''))
        tmp = self.cfg["esxi"]["password"].split(',')
        for password in tmp:
            password = password.lstrip()
            settings["esxi"]["password"].append(password.replace("\\\n", ''))
        tmp = self.cfg["esxi"]["tcpdump"].split(',')
        for cmd in tmp:
            cmd = cmd.lstrip()
            settings["esxi"]["tcpdump"].append(cmd.replace("\\\n", ''))
        tmp = self.cfg["esxi"]["pktcap"].split(',')
        for cmd in tmp:
            cmd = cmd.lstrip()
            settings["esxi"]["pktcap"].append(cmd.replace("\\\n", ''))

    def init(self, settings):
        if not self.cfg.has_section("default"):
            self.cfg.add_section("default")
        self.cfg["default"]["wiresharkPath"] = settings["default"]["wiresharkPath"]
        sett = deepcopy(settings)
        if not self.cfg.has_section("linux"):
            self.cfg.add_section("linux")
        self.cfg["linux"]["host"] = ','.join(sett["linux"]["host"])
        self.cfg["linux"]["port"] = ','.join(sett["linux"]["port"])
        self.cfg["linux"]["user"] = ','.join(sett["linux"]["user"])
        self.cfg["linux"]["password"] = ','.join(sett["linux"]["password"])
        self.cfg["linux"]["su_user"] = ','.join(sett["linux"]["su_user"])
        self.cfg["linux"]["su_password"] = ','.join(sett["linux"]["su_password"])
        self.cfg["linux"]["cmd"] = ','.join(sett["linux"]["cmd"])

        if not self.cfg.has_section("esxi"):
            self.cfg.add_section("esxi")
        self.cfg["esxi"]["host"] = ','.join(sett["esxi"]["host"])
        self.cfg["esxi"]["port"] = ','.join(sett["esxi"]["port"])
        self.cfg["esxi"]["user"] = ','.join(sett["esxi"]["user"])
        self.cfg["esxi"]["password"] = ','.join(sett["esxi"]["password"])
        self.cfg["esxi"]["tcpdump"] = ','.join(sett["esxi"]["tcpdump"])
        self.cfg["esxi"]["pktcap"] = ','.join(sett["esxi"]["pktcap"])

        with open(self.configPath, 'w', encoding="utf-8") as f:
            self.cfg.write(f)

    def write(self, settings):
        self.cfg["default"]["wiresharkPath"] = settings["default"]["wiresharkPath"]
        sett = deepcopy(settings)
        # if len(sett["linux"]["host"]) > 0:
        #     sett["linux"]["host"].pop(0)
        self.cfg["linux"]["host"] = ','.join(sett["linux"]["host"])
        self.cfg["linux"]["port"] = ','.join(sett["linux"]["port"])
        self.cfg["linux"]["user"] = ','.join(sett["linux"]["user"])
        self.cfg["linux"]["password"] = ','.join(sett["linux"]["password"])
        self.cfg["linux"]["su_user"] = ','.join(sett["linux"]["su_user"])
        self.cfg["linux"]["su_password"] = ','.join(sett["linux"]["su_password"])
        self.cfg["linux"]["cmd"] = ','.join(sett["linux"]["cmd"])

        self.cfg["esxi"]["host"] = ','.join(sett["esxi"]["host"])
        self.cfg["esxi"]["port"] = ','.join(sett["esxi"]["port"])
        self.cfg["esxi"]["user"] = ','.join(sett["esxi"]["user"])
        self.cfg["esxi"]["password"] = ','.join(sett["esxi"]["password"])
        self.cfg["esxi"]["tcpdump"] = ','.join(sett["esxi"]["tcpdump"])
        self.cfg["esxi"]["pktcap"] = ','.join(sett["esxi"]["pktcap"])

        with open(self.configPath, 'w',  encoding="utf-8") as f:
            self.cfg.write(f)
