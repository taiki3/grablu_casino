# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

option = {
    "compressed"    :    1    ,
    "optimize"      :    2    ,
    "bundle_files"  :    2
}

setup(
    options = {
        "py2exe" : {"includes" : ["sip"]}

    },

    windows = [{
        'script' : 'windowsGUI.py',
        'icon_resources' : [(1,"icon.ico")],
        'dest_base' : 'GranBlueChondro'
    }],

    zipfile = 'lib\libs.zip',
    version = '0.9.2',
    name = 'GranBlue Chondro',
    description="GranBlue Casino Macro",
    author="UNKNOWN",
)
