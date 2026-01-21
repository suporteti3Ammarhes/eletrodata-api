import requests
import xml.etree.ElementTree as ET
import html


class SOAPClient:
    
    def __init__(self, url: str, headers: dict, sistema: str, db_service=None):
        self.url = url
        self.headers = headers
        self.sistema = sistema
        self.db_service = db_service
    def executar(self, consulta, parametros: str):
        payload = f"""<?xml version="1.0" encoding="utf-8"?>
                        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                                          xmlns:tot="http://www.totvs.com/">
                          <soapenv:Header/>
                          <soapenv:Body>
                            <tot:RealizarConsultaSQL>
                              <tot:codSentenca>{consulta.sentenca}</tot:codSentenca>
                              <tot:codSistema>{self.sistema}</tot:codSistema>
                              <tot:parameters>{parametros}</tot:parameters>
                            </tot:RealizarConsultaSQL>
                          </soapenv:Body>
                        </soapenv:Envelope>"""
        
        response = requests.post(self.url, headers=self.headers, data=payload, timeout=30)
        response.raise_for_status()
        
        return self._processar_resposta(response.text, consulta.campos, consulta.processar_status, consulta.table)
    
    def _processar_resposta(self, response_text: str, campos: list, processar_status: bool = False, table: str = ""):
      with open('response.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(response_text)
      
      root = ET.fromstring(response_text)
      
      ns = {
        's': 'http://schemas.xmlsoap.org/soap/envelope/',
        't': 'http://www.totvs.com/'
      }
      
      resultado = root.find('.//t:RealizarConsultaSQLResult', ns)
      
      if resultado is None or not resultado.text:
        print("[DEBUG] Nenhum resultado encontrado")
        return []
      
      xml_interno = html.unescape(resultado.text)
      print(f"[DEBUG] XML Interno:\n{xml_interno}")
      
      root_interno = ET.fromstring(xml_interno)
      
      resultados = []
      for item in root_interno.findall('Resultado'):
        registro = {campo.lower(): item.findtext(campo) for campo in campos}
        if processar_status:
          registro['status'] = "DEMITIDO" if registro.get('datademissao') else "ADMITIDO"
        resultados.append(registro)
      
      if self.db_service and table and resultados:
        self.db_service.insert_batch(table, resultados)
      
      print(f"[DEBUG] Total de registros processados: {len(resultados)}")
      return resultados
