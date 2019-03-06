# -*- coding: utf-8 -*-
#this code gets data which is made by HTML,XML format

import urllib.request

def get_data(URL):
    return urllib.request.urlopen(URL).read()