#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

def get_key_value(reservatorio, key):
    if r.hexists(reservatorio, key):
        return r.hget(reservatorio, key)
    return ''


# dado em %
def get_volume_armazenado(reservatorio):
    return get_key_value(reservatorio, 'volume armazenado')


# dado em mm
def get_pluviometria_dia(reservatorio):
    return get_key_value(reservatorio, 'pluviometria do dia')


# dado em mm
def get_pluviometria_acumulada_mes(reservatorio):
    return get_key_value(reservatorio, 'pluviometria acumulada no mês')


# dado em mm
def get_media_historica(reservatorio):
    return get_key_value(reservatorio, 'média histórica do mês')


# dado em mm
def get_name(reservatorio):
    return get_key_value(reservatorio, 'name')


def criar_reservatorios():
    sabesp_api = requests.get("https://sabesp-api.herokuapp.com/")
    for reservatorio in sabesp_api.json():
        r.hset('reservatorio:' + reservatorio['name'], 'name', reservatorio['name'])
        for dados_reservatorio in reservatorio['data']:
            value = dados_reservatorio['value']
            value = value.replace(',', '.')
            value = re.sub(r'[^\d\.]+', '', value)
            print value
            r.hset('reservatorio:' + reservatorio['name'], dados_reservatorio['key'], value)
            print r.hgetall('reservatorio:' + reservatorio['name'])
    

def get_reservatorios():
    reservatorios = r.keys('reservatorio:*')
    if reservatorios:
        return reservatorios
    return ''


def main():
    # criando reservatorios
#    criar_reservatorios()
#    return

    #recuperando os dados dos reservatorios
    reservatorios = r.keys('reservatorio:*')
    for res in reservatorios:
        print get_name(res)
        print get_volume_armazenado(res)
        print get_media_historica(res)
        print get_pluviometria_dia(res)
        print get_pluviometria_acumulada_mes(res)


if __name__ == "__main__":
    main()
