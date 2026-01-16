import requests

url = "http://rm.eletrodataengenharia.com.br:8051/wsConsultaSQL/IwsConsultaSQL"

headers = {
    "Content-Type": "text/xml; charset=utf-8",
    "Accept": "text/xml",
    "SOAPAction": "http://www.totvs.com/IwsConsultaSQL/RealizarConsultaSQL",
    "Authorization": "Basic YW1tYXJoZXM6RWxldHJvMjU="
}

soap_body = """<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:tot="http://www.totvs.com/">
  <soapenv:Header/>
  <soapenv:Body>
    <tot:RealizarConsultaSQL>
      <tot:codSentenca>ammarhes.importa</tot:codSentenca>
      <tot:codColigada>3</tot:codColigada>
      <tot:codSistema>P</tot:codSistema>
      <tot:parameters></tot:parameters>
    </tot:RealizarConsultaSQL>
  </soapenv:Body>
</soapenv:Envelope>
"""

response = requests.post(url, headers=headers, data=soap_body, timeout=30)

print("Status:", response.status_code)
print("Resposta:")
print(response.text)
