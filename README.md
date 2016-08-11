# Vereadores SP

A história desses scripts estão nesse texto:

http://bit.ly/2bjB1nl

Exemplos de uso...

Convertendo o arquivo TXT em JSON:
```
$ ./ver2json.py <vereadores.txt  >vereadores.json
```

Lendo o registro da 205ª linha do TXT em JSON:
```
$ head -205 vereadores.txt | tail -2 | ./ver2json.py | ./prettify.py 
[
    {
        "Registro": 40208,
        "Nome": "Waldir da Silva Prado",
        "Lideranca": [],
        "NomeParlamentar": [
            "Waldir da Silva Prado"
        ],
        "Vereancas": [
            {
                "Partido": "PTN",
                "NomeVereadorSaiu": "Venicio Camillo Giachini",
                "VereancaDataIn": "11/10/1961",
                "situacao": "suplente",
                "VereancaDataFin": "09/11/0961"
            }
        ],
        "ComissoesPermanentes": [],
        "Legislaturas": [
            {
                "QuantVotos": 2786,
                "PeriodoHistorico": 3,
                "Situacao": "Suplente",
                "NumeroLegislatura": 4
            }
        ],
        "MesaDiretora": []
    }
]
```
Checando com a linha original:
```
$ head -205 vereadores.txt | tail -1 
40208#Waldir da Silva Prado#####^p3^n4^sSuplente^q2786%#^i11/10/1961^f09/11/0961^ssuplente^pPTN^bVenicio Camillo Giachini%#
```
O `tail -2` no primeiro caso se faz necessário pois o script `ver2json.py` sempre desconsidera a primeira linha esperando nela o cabeçalho.
