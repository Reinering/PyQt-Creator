#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


from oslo_config import cfg


CONF = cfg.CONF

# Define an option group
default = cfg.OptGroup("default")
wiresharkPath = cfg.StrOpt("wiresharkPath", help="wireshark path")
CONF.register_group(default)
cfg.CONF.register_opt(wiresharkPath, group=default)

linux = cfg.OptGroup("linux")
host = cfg.ListOpt("host", help="host")
port = cfg.ListOpt("port", help="port")
user = cfg.ListOpt("user", help="user")
password = cfg.ListOpt("password", help="password")
su_user = cfg.ListOpt("su_user", help="su user")
su_password = cfg.ListOpt("su_password", help="su password")
cmd = cfg.ListOpt("cmd", help="cmd")
CONF.register_group(linux)
cfg.CONF.register_opt(host, group=linux)
cfg.CONF.register_opt(port, group=linux)
cfg.CONF.register_opt(user, group=linux)
cfg.CONF.register_opt(password, group=linux)
cfg.CONF.register_opt(su_user, group=linux)
cfg.CONF.register_opt(su_password, group=linux)
cfg.CONF.register_opt(cmd, group=linux)

esxi = cfg.OptGroup("esxi")
host = cfg.ListOpt("host", help="host")
port = cfg.ListOpt("port", help="port")
user = cfg.ListOpt("user", help="user")
password1 = cfg.ListOpt("password", help="password")
cmd = cfg.ListOpt("cmd", help="cmd")
CONF.register_group(esxi)
cfg.CONF.register_opt(host, group=esxi)
cfg.CONF.register_opt(port, group=esxi)
cfg.CONF.register_opt(user, group=esxi)
cfg.CONF.register_opt(password, group=esxi)
cfg.CONF.register_opt(cmd, group=esxi)


# default = cfg.OptGroup("default")
# origin = cfg.StrOpt("origin", help="domain name")
# ipaddr = cfg.StrOpt("ipaddr", help="server ip address")
# pollingTime = cfg.IntOpt("pollingTime", help="polling time")
# server = cfg.DictOpt("server", help="server config list")
# CORS_LIST = cfg.ListOpt("CORS_LIST", help="CORS list")
# # Register your config group
# CONF.register_group(default)
# # Register your options within the config group
# CONF.register_opt(origin, group=default)
# CONF.register_opt(ipaddr, group=default)
# CONF.register_opt(pollingTime, group=default)
# CONF.register_opt(server, group=default)
# CONF.register_opt(CORS_LIST, group=default)


