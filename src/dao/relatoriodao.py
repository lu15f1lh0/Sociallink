from dao.db import *
from model.entities import *

class RelatorioDAO:
  def __init__(self):
    self.connection = createConnection()

  def create(self, dis, us):
    cursor = self.connection.cursor()   
    sql = 'insert into relatorio(codigo_us, nome_us, qtd_vz_tp) values (%s, %s, %s)' % (us.codigo, us.nome, 1)
    l = self.cursor.execute(sql)
    self.connection.commit()
    cursor.close()

  def search(self, longitude, latitude):
    """Criar o objeto de pesquisa LocalizacaoGeografica"""
    locGeo = LocalizacaoGeografica(longitude, latitude)
	
    """Guardar o id do Objeto mais proximo"""
    id = 0;

    """Guardar a menor distancia encontrada"""
    dist = 99999999999999999999999999999999999999999999999999.9

    """Guarda objeto mais proximo"""
    locGeoProximo = LocalizacaoGeografica(None, None)

    cursor = self.connection.cursor()
    sql = "select * from LocalizacaoGeografica"
    cursor.execute(sql)
    """Pesquisar todos os valores e destacar o mais o proximo"""
    for row in cursor.fetchall():
      l = append(LocalizacaoGeografica(row[1], row[2]))
      distC = locGeo.dist(l)
      if (distC < dist):
        dist = distC
        id = row[0]
        locGeoProximo = l
    
    obj = {"dist": dist,
           "obj": locGeoProximo
    }
    cursor.close()
    return obj
	

  def delete(self, idLocGeo):
    pass

  def update(self, locGeo):
    pass

  def searchAll(self):
    cursor = self.connection.cursor()
    sql = "select * from LocalizacaoGeografica"
    cursor.execute(sql)
    result = []
    for row in cursor.fetchall():
      result.append(LocalizacaoGeografica(row[1], row[2]))
    cursor.close()
    return result