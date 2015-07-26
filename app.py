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
        res = 'reservatorio:Alto Cotia'
        nivel_perc_reservatorio = sabesp.get_volume_armazenado(res)
        
        texto_reservatorio = 'Tá chovendo'
        img_chovendo = 'img/tempo-02.png'

        #img_chovendo = 'img/tempo-01.png'
        #texto_reservatorio = 'Não tá chovendo'

        txt_nivel_reservatorio = nivel_perc_reservatorio + ' %'

        acm_mes = sabesp.get_volume_armazenado(res)
        media_historica = sabesp.get_media_historica(res)
        nivel_chuva = int((float(acm_mes) / float(media_historica)) / 0.20)
        if nivel_chuva > 5:
            nivel_chuva = 5

        txt_nivel_chuva = float(acm_mes) / float(media_historica)

        return tmpl.render(title = 'Hello World!',
            nivel_reservatorio = 'img/escala_emotion-0' + str(int(float(nivel_perc_reservatorio) / 20)) + '.png',
            img_chovendo = img_chovendo,
            texto_reservatorio = texto_reservatorio.decode('utf-8'),
            txt_nivel_reservatorio = txt_nivel_reservatorio.decode('utf-8'),
            nivel_chuva = 'img/bilu_emotion-0' + str(nivel_chuva) + '.png',
            txt_nivel_chuva = txt_nivel_chuva)

cherrypy.quickstart(App(), '/', config.CHERRYPY_CONFIG)
