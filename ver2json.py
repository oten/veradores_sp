#!/usr/bin/env python
#coding: utf-8
import sys
import re
import json
import codecs
from collections import namedtuple


Field = namedtuple('Field', 'name regex type')
Section = namedtuple('Section', 'name regex fields')

sections = [
#Referencia no cabeçalho
#LiderPartido^iDataIn^fDataFin^cCargo
Section('Lideranca',
         ur'(%|##)[^\^]*\^i\d{2}/\d{2}/\d{4}\^f\d{2}/\d{2}/\d{4}\^c[^\^%]*',
         [Field('LiderPartido', ur'^[#%][^\^]*\^i', unicode),
          Field('DataIn', ur'\^i[^\^]*', unicode),
          Field('DataFin', ur'\^f[^\^]*', unicode),
          Field('Cargo', ur'\^c[^\^]*', unicode),]),

#Referencia no cabeçalho
#^cMesaCargo^iInicioCargo^fFimCargo^bObservacao
Section('MesaDiretora',
         ur'\^c[^\^]*\^i\d{2}/\d{2}/\d{4}\^f\d{2}/\d{2}/\d{4}(\^b[^\^]*|)',
         [Field('MesaCargo', ur'\^c[^\^]*', unicode),
          Field('InicioCargo', ur'\^i[^\^]*', unicode),
          Field('FimCargo', ur'\^f[^\^]*', unicode),
          Field('Observacao', ur'\^b[^\^]*', unicode),]),

#Referencia no cabeçalho
#^pPeriodoHistorico^nNumeroLegislatura^sSituacao^qQuantVotos
Section('Legislaturas',
         ur'\^p[123]\^n\d*\^s(Vereador|Suplente|Cassado)(\^q[^\^]*|)',
         [Field('PeriodoHistorico', ur'\^p[^\^]*', int),
          Field('NumeroLegislatura', ur'\^n[^\^]*', int),
          Field('Situacao', ur'\^s[^\^]*', unicode),
          Field('QuantVotos', ur'\^q[^\^]*', lambda q: int(filter(unicode.isdigit, q))),]),

#Referencia no cabeçalho
#^iVereancaDataIn^fVereancaDataFin^situacao^pPartido^bNomeVereadorSaiu^cObsPartido^dObsVereanca
Section('Vereancas', 
         ur'\^i\d{2}/\d{2}/\d{4}\^f\d{2}/\d{2}/\d{4}\^s(vereador|suplente|cassado)(\^p[^#%\^]*|)(\^b[^#%\^]*|)(\^c[^#%\^]*|)(\^d[^#%\^]*|)',
         [Field('VereancaDataIn', ur'\^i[^\^]*', unicode),
          Field('VereancaDataFin', ur'\^f[^\^]*', unicode),
          Field('situacao', ur'\^s[^\^]*', unicode),
          Field('Partido', ur'\^p[^\^]*', unicode),
          Field('NomeVereadorSaiu', ur'\^b[^\^]*', unicode),
          Field('ObsPartido', ur'\^c[^\^]*', unicode),
          Field('ObsVereanca', ur'\^d[^\^]*', unicode),]),

#Referencia no cabeçalho
#^nComissaoNome^iDataIn^fDataFin^cCargo^dObs
Section('ComissoesPermanentes',
         ur'\^n[^\^]*\^i\d{2}/\d{2}/\d{4}\^f\d{2}/\d{2}/\d{4}\^c[^\^]*(\^d[^\^]*|)',
         [Field('ComissaoNome', ur'\^n[^\^]*', unicode),
          Field('DataIn', ur'\^i[^\^]*', unicode),
          Field('DataFin', ur'\^f[^\^]*', unicode),
          Field('Cargo', ur'\^c[^\^]*', unicode),
          Field('Obs', ur'\^d[^\^]*', unicode),]),
]


def matches_to_dicts(matches, fields):
    dicts = list()
    for m in matches:
        data = dict()
        for field in fields:
            field_match = re.search(field.regex, m.group())
            if field_match:
                value = field_match.group()
                value = re.sub(r'(\^.|[%#])', '', value) #limpa
                value = field.type(value)                #converte  
                data.update({field.name: value})
        dicts.append(data)
    return dicts


if __name__ == "__main__":
    if len(sys.argv) != 1:
        sys.stderr.write('usage:\n')
        sys.stderr.write('    {} <vereador.txt >vereador.json\n'.format(sys.argv[0]))
        sys.exit(-1)
    
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    
    text = sys.stdin.read()
    
    #Todas as linhas menos o cabecalho e a última string que é vazia pois o arquivo acaba com um '\n'.
    rows = [row for row in text.split('\n') if row and re.search(ur'^[0-9]', row)]
    
    data_list = [{section.name: matches_to_dicts(re.finditer(section.regex, row), section.fields) for section in sections} for row in rows]
    
    #Registro, Nome e NomeParlamentar mais sussa fazer com split mesmo do que com regex.
    #Referencia no cabeçalho
    #Registro#Nome#NomeParlamentar
    for data, row in zip(data_list, rows):
        data.update({'Registro': int(row.split('#')[0]),
                     'Nome': row.split('#')[1],
                     'NomeParlamentar': row.split('##')[0].split('#')[-1].split('%')})

    sys.stdout.write(json.dumps(data_list, ensure_ascii=False))
