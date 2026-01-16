import requests

url = "http://rm.eletrodataengenharia.com.br:8051/wsConsultaSQL/IwsConsultaSQL"

headers = {
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": "http://www.totvs.com/IRMSServer/CheckServiceActivity",
    "Authorization": "Basic YW1tYXJoZXM6RWxldHJvMjU="
}

soap_body = """<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:tot="http://www.totvs.com/">
  <soapenv:Header/>
  <soapenv:Body>
    <tot:CheckServiceActivity/>
  </soapenv:Body>
</soapenv:Envelope>
"""

resp = requests.post(url, headers=headers, data=soap_body, timeout=15)

print(resp.status_code)
print(resp.text)
