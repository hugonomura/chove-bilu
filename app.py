#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from _config import app_conf as config
from _config import secrets as secret
from os import path
from jinja2 import Environment, FileSystemLoader
from crawlers import sabesp as sabesp

env = Environment(loader = FileSystemLoader('static'))

class App(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('html.html')
        
        reservatorios = sabesp.get_reservatorios()

        lista_reservatorios = []
        for reservatorio in reservatorios:
            print '---> ' + sabesp.get_name(reservatorio)
            nome = sabesp.get_name(reservatorio)
            lista_reservatorios.append({'nome': nome.decode('utf-8'), 'id': reservatorio.decode('utf-8')})


        return tmpl.render(title = 'Hello World!',
            reservatorios = lista_reservatorios,
            nivel_reservatorio = 'img/escala_emoticon-01.png')

    @cherrypy.expose
    def main(self):
        tmpl = env.get_template('main.html')
        nivel_perc_reservatorio = sabesp.get_volume_armazenado('reservatorio:Alto Cotia')

        return tmpl.render(title = 'Hello World!',
            nivel_reservatorio = 'img/escala_emotion-0' + str(int(float(nivel_perc_reservatorio) / 20)) + '.png')

cherrypy.quickstart(App(), '/', config.CHERRYPY_CONFIG)
