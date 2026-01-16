import requests

url = "http://rm.eletrodataengenharia.com.br:8051/wsConsultaSQL/IwsConsultaSQL"

headers = {
    "Content-Type": "text/xml; charset=utf-8",
    "Accept": "text/xml",
    "SOAPAction": "http://www.totvs.com/IwsBase/AutenticaAcesso",
    "Authorization": "Basic YW1tYXJoZXM6RWxldHJvMjU="
}

soap_body = """<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:tot="http://www.totvs.com/">
  <soapenv:Header/>
  <soapenv:Body>
    <tot:AutenticaAcesso/>
  </soapenv:Body>
</soapenv:Envelope>
"""

response = requests.post(
    url,
    headers=headers,
    data=soap_body,
    timeout=15
)

print("Status:", response.status_code)
print("Resposta:")
print(response.text)
