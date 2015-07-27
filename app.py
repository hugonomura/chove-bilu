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
        tmpl = env.get_template('index.html')
        
        reservatorios = sabesp.get_reservatorios()

        lista_reservatorios = []
        for reservatorio in reservatorios:
            print '---> ' + sabesp.get_name(reservatorio)
            nome = sabesp.get_name(reservatorio)
            if(nome == 'Alto Tietê'):
                continue
            lista_reservatorios.append({'nome': nome.decode('utf-8'), 'id': reservatorio.decode('utf-8')})


        return tmpl.render(
            reservatorios = lista_reservatorios)


    @cherrypy.expose
    def main(self, reservatorio):
        tmpl = env.get_template('main.html')
        print reservatorio
        #res = 'reservatorio:Rio Claro'
        res = str(reservatorio.decode('utf-8'))
        print '-----> ' + res
        nivel_perc_reservatorio = sabesp.get_volume_armazenado(res)
        
        acm_dia = sabesp.get_pluviometria_dia(res)
        print '-----> ' + str(acm_dia)
        if float(acm_dia) > 7.0:
            texto_reservatorio = 'Tá chovendo'
            img_chovendo = 'img/tempo-02.png'
        else:
            img_chovendo = 'img/tempo-01.png'
            texto_reservatorio = 'Não tá chovendo'

        txt_nivel_reservatorio = nivel_perc_reservatorio + ' %'

        acm_mes = sabesp.get_volume_armazenado(res)
        media_historica = sabesp.get_media_historica(res)
        nivel_chuva = int((float(acm_mes) / float(media_historica)) / 0.20)
        if nivel_chuva > 5:
            nivel_chuva = 5

        txt_nivel_chuva = float(acm_mes) / float(media_historica)

        return tmpl.render(
            nivel_reservatorio = 'img/escala_emotion-0' + str(int(float(nivel_perc_reservatorio) / 20)) + '.png',
            img_chovendo = img_chovendo,
            texto_reservatorio = texto_reservatorio.decode('utf-8'),
            txt_nivel_reservatorio = txt_nivel_reservatorio.decode('utf-8'),
            nivel_chuva = 'img/bilu_emoticons-0' + str(nivel_chuva) + '.png',
            txt_nivel_chuva = str(int(txt_nivel_chuva * 100)) + ' %')


cherrypy.quickstart(App(), '/', config.CHERRYPY_CONFIG)
