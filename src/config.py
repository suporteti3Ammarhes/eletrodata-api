SOAP_CONFIG = {
    "url": "http://rm.eletrodataengenharia.com.br:8051/wsConsultaSQL/IwsConsultaSQL",
    "headers": {
        'Authorization': 'Basic YW1tYXJoZXM6RWxldHJvMjU=',
        'SOAPAction': 'http://www.totvs.com/IwsConsultaSQL/RealizarConsultaSQL',
        'Content-Type': 'text/xml; charset=utf-8;',
        'Accept': 'text/xml'
    },
    "sistema": "P"
}

CONSULTAS_CONFIG = {
    "planilha_importacao": {
        "sentenca": "ammarhes.importa",
        "parametros_fixos": "CODCOLIGADA=3",
        "campos": ['NOME', 'CHAPA', 'DTNASCIMENTO', 'CPF', 'PISPASEP', 'CODCARGO', 
                   'CODFUNCAO', 'CBO', 'FUNCAO', 'DATAADMISSAO', 'SETOR', 
                   'SUBSETOR', 'CODCCUSTO', 'NOME1'],
        "requer_periodo": False,
        "table": "amm_importacao_eletrodata"
    },
    "admitidos_demitidos": {
        "sentenca": "ammarhes.adm.dem",
        "parametros_fixos": "CODCOLIGADA=3",
        "campos": ['NOME', 'CHAPA', 'DTNASCIMENTO', 'CPF', 'PISPASEP', 'CODCARGO', 
                   'CODFUNCAO', 'CBO', 'FUNCAO', 'DATAADMISSAO', 'DATADEMISSAO', 'SETOR', 
                   'SUBSETOR', 'CODCCUSTO', 'NOME1'],
        "requer_periodo": True,
        "processar_status": True,
        "table": "amm_eletrodata_admitidos_demitidos"
    },
    "realocados": {
        "sentenca": "ammarhes.realoca",
        "parametros_fixos": "CODCOLIGADA=3",
        "campos": ['NOME', 'CHAPA', 'DTNASCIMENTO', 'CPF', 'PISPASEP', 'CODCARGO', 
                   'CODFUNCAO', 'CBO', 'FUNCAO', 'DATAADMISSAO', 'SETOR', 
                   'SUBSETOR', 'CODCCUSTO', 'NOME1'],
        "requer_periodo": True,
        "table": "amm_eletrodata_realocados"
    },
    "funcoes": {
        "sentenca": "ammarhes.funcao",
        "parametros_fixos": "CODCOLIGADA=3",
        "campos": ['CODIGO', 'NOME', 'DESCRICAO'],
        "requer_periodo": True,
        "table": "amm_eletrodata_funcoes"
    },
    "cargos": {
        "sentenca": "ammarhes.cargo",
        "parametros_fixos": "CODCOLIGADA=3",
        "campos": ['CODIGO', 'NOME', 'DESCRICAO'],
        "requer_periodo": True,
        "table": "amm_eletrodata_cargos"
    },
    "tomadores": {
        "sentenca": "ammarhes.tomador",
        "parametros_fixos": "CODCOLIGADA=3",
        "campos": ['CODIGO', 'NOME', 'CNPJ', 'ENDERECO'],
        "requer_periodo": False,
        "table": "amm_eletrodata_tomadores"
    }
}
