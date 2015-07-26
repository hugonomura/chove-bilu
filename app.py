#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from _config import app_conf as config
from _config import secrets as secret
from os import path
from jinja2 import Environment, FileSystemLoader

env = Environment(loader = FileSystemLoader('static'))

class App(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(title = 'Hello World!')


cherrypy.quickstart(App(), '/', config.CHERRYPY_CONFIG)
