from flask import Flask, jsonify, request
from flask_cors import CORS
from .soap_client import SOAPClient
from .service import ConsultaService
from .db import DatabaseService
from .config import SOAP_CONFIG, CONSULTAS_CONFIG

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    db_service = DatabaseService()
    soap_client = SOAPClient(SOAP_CONFIG["url"], SOAP_CONFIG["headers"], SOAP_CONFIG["sistema"], db_service)
    service = ConsultaService(soap_client, CONSULTAS_CONFIG)
    
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            "nome": "API TOTVS RM - Eletrodata",
            "versao": "2.0.0",
            "endpoints": {
                "listar": "/api/consultas",
                "executar": "/api/consulta/<nome>",
                "health": "/health"
            }
        })
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"})
    
    @app.route('/api/consultas', methods=['GET'])
    def listar_consultas():
        try:
            consultas = service.listar_consultas()
            return jsonify({"total": len(consultas), "consultas": consultas})
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
    
    @app.route('/api/consulta/<nome_consulta>', methods=['GET'])
    def executar_consulta(nome_consulta):
        try:
            mes = request.args.get('mes')
            ano = request.args.get('ano')
            resultado = service.executar_consulta(nome_consulta, mes, ano)
            
            return jsonify({
                "consulta": resultado.consulta,
                "sentenca": resultado.sentenca,
                "parametros": resultado.parametros,
                "total_registros": resultado.total_registros,
                "timestamp": resultado.timestamp,
                "dados": resultado.dados
            })
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
    
    return app
