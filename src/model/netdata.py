'''
Created on 9 de mar de 2017

Obtem dados em arquivos da internet

@author: Gilzamir (gilzamir@outlook.com)
'''

#coding: utf-8

import urllib.request as request
import zipfile
import io
import os
import re
import model
import sys
import math


class NetDataModel(Exception):

    def download_length(self, response, output, length):
        times = length/BUFF_SIZE
        if length % BUFF_SIZE > 0:
            times = times + 1
        for time in range(int(times)):
            output.write(response.read(BUFF_SIZE))
            print("Downloaded %d " % (((time * BUFF_SIZE)/100.0) * 100))

    def download(self, response, output):
        total_downloaded = 0
        while True:
            data = response.read(BUFF_SIZE)
            total_downloaded += len(data)
            if not data:
                break
            output.write(data)
            print('Downloaded {bytes}'.format(bytes=total_downloaded))

    def extract_filename(self, filename):
        filename = filename.split('.')
        del filename[len(filename) - 1]
        return '.'.join(filename)

    def read_data(self, path):
        fdata = open(path, 'rt', encoding="utf8")
        data = []
        for line in fdata:
            ld = line.split(',')
            
            ender = model.Endereco(ld[5], ld[6], ld[7], ld[8])
            unit_health = model.UnidadeDeSaude(ld[0], ld[1], ld[2], ld[3], ld[4], ender, ld[9], ld[10], ld[11], ld[12])
            
            data.append(unit_health)
        fdata.close()
        return data

    def validarTelefone(self, telefone):
        if not re.match('\(\d{2}\)\d{8,9}$', telefone):
            raise model.NumeroTelefoneInvalido(telefone, "Telefone Inválido")

    def loadlistfromcsv(self, URL, OUTPUT_PATH="dt.zip", EXTRACTION_PATH="./"):
        zfile = zipfile.ZipFile(OUTPUT_PATH)
        zfile.extractall(EXTRACTION_PATH)
        filename = [name for name in os.listdir(EXTRACTION_PATH) if '.csv' in name]
        dt = self.read_data(EXTRACTION_PATH+filename[0])
      
        return dt

    def create_cidcnes_index(self, list):
        db = {}
        for obj in list:
            cidval = obj.magicGet('codCid')
            cnesval = obj.magicGet('codCnes')
            print(type(obj))
            db[cidval+cnesval] = obj
        return db;

    def create_index_from(self, source, col_index):
        db = {}
        for obj in source:
            index = ""
            for key in col_index:
                index += obj.magicGet(key)
            db[index] = obj
        return db;

    def interpret(self, line_from_source, col_index, **kargs):
        line = []
        for key in kargs:
            idx = col_index[key]
            coltype = kargs[key]
            line.append(coltype(line_from_source[idx]))
        return line

    def syncdata(self):
        RESOURCE_URL = "http://repositorio.dados.gov.br/saude/unidades-saude/unidade-basica-saude/ubs.csv.zip"

        if os == "Windows":
            OUTPUT_PATH = os.path.expanduser("saida.zip")
            EXTRACTED_PATH = os.path.expanduser("~\\")
        else:
            OUTPUT_PATH = os.path.expanduser("saida.zip")
            EXTRACTED_PATH = os.path.expanduser("~/")

        if len(sys.argv) > 1:
            RESOURCE_URL = sys.argv[1] 
        if len(sys.argv) > 2:
            OUTPUT_PATH = sys.argv[2]
        if len(sys.argv) > 3:
            EXTRACTION_PATH = sys.argv[3]
        self.repository = self.loadlistfromcsv(RESOURCE_URL, OUTPUT_PATH, EXTRACTED_PATH)

    
    def distancia_geodesica(self, la1, la2, lo1, lo2):
        raio_terra = 6371
        dlat = la2 - la1
        dlon = lo2 - lo1
        a = math.sin(dlat/2)**2 + math.cos(la1) * math.cos(la2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return c * raio_terra


    def searchNearUnitHealth(self, longitude, latitude):
        v = []
        
        h_u = self.repository
        raio_terra = 6378.1
        
        min_dis = 999999999999999999999999999999999999999999999999
        near_unit = h_u[1]
    
        i = 0
        for u in h_u:
           if (i > 0):
              la = float(u.latitude)
              lo = float(u.longitude)
              dis = self.distancia_geodesica (latitude, la, longitude, lo)
              t = {'dis':dis, 'uni':u}
              v.append(t)
  
           i = i+1
        
        v.sort(key=lambda a: a['dis'])
        i = 0
        
        cnes = v[i]['uni']._get_cnes()

        la = v[i]['uni'].latitude
        lo = v[i]['uni'].longitude

        try :
          self.dicio[la+lo]['qtd_vz'] = self.dicio[la+lo]['qtd_vz'] + 1
        except Exception as e:
          self.dicio[la+lo] = {'cnes': cnes, 'nome': v[i]['uni']._get_nome(), 'qtd_vz': 1}
        stt = ""
        i = 0
        stt = "Unidade mais próxima: \n"+"Latitude: " + str(v[i]['uni'].latitude)+ " Longitude: " + str(v[i]['uni'].longitude) + " \n" + "Distância: " + str(v[i]['dis']) + "u.d \n"+"Logradouro:"+ v[i]['uni']._get_endereco()._get_logadouro() + " \n"+"Bairro: "+ v[i]['uni']._get_endereco()._get_bairro() + " \n"+ "Cidade: "+ v[i]['uni']._get_endereco()._get_cidade()+ " \n" + str(self.dicio[v[i]['uni'].latitude + v[i]['uni'].longitude]['qtd_vz'])+" \n"
        """print(stt)"""
        """print("Unidade mais próxima: \n")
        print ("Latitude: " + v[i]['uni'].latitude + " Longitude: " + v[i]['uni'].longitude + " \n")
              print ("Logradouro: " + v[i]['uni']._get_endereco()._get_logadouro() + " \n")
              print ("Bairro: " + v[i]['uni']._get_endereco()._get_bairro() + " \n")
              print ("Cidade: " + v[i]['uni']._get_endereco()._get_cidade() + " \n")
              print (self.dicio[v[i]['uni'].latitude + v[i]['uni'].longitude]['qtd_vz'])
              print (" \n")"""
        return stt
        
    def searchAllUnitHealth(self):
        h_u = self.repository
        return h_u
        i = 0
        string = []
        for u in h_u:
           if i > 0:
              stt = ""
              stt = "Latitude: " + str(u.latitude) + " Longitude: " + str(u.longitude) + " \n" + "Logradouro: " + u._get_endereco()._get_logadouro() + " \n" + "Bairro: " + u._get_endereco()._get_bairro() + " \n" + "Cidade: " + u._get_endereco()._get_cidade() + " \n" + "____________________________________________________________________________________________________________________________\n\n\n"
              string.append(stt)
              """print(stt)"""
              """print ("Latitude: " + u.latitude + " Longitude: " + u.longitude + " \n")
              print ("Logradouro: " + u._get_endereco()._get_logadouro() + " \n")
              print ("Bairro: " + u._get_endereco()._get_bairro() + " \n")
              print ("Cidade: " + u._get_endereco()._get_cidade() + " \n")
              print ("____________________________________________________________________________________________________________________________\n\n\n")"""
           i = i + 1
               
        return string
           
       

    def generateLog(self):
        d = []
        for obj in self.dicio:
            d.append(self.dicio[obj])
        
        d.sort(key=lambda a: a['qtd_vz'])

        for e in d:
            print('Cnes: ' + e['cnes'])
            print('Nome: ' + e['nome'])
            print('Quantidade de vezes entre os três mais próximos na busca: ' + str(e['qtd_vz']))
            print('__________________________________________________________________________\n\n')


    def __init__(self):
        self.repository = []
        self.dicio = {}
