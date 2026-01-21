import os
import logging
from dotenv import load_dotenv

# Carrega .env PRIMEIRO, antes de qualquer outra importação
load_dotenv()

from src.app import create_app
from src.db import DatabaseService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database_connection():
    try:
        db = DatabaseService()
        if db.test_connection():
            return True
        else:
            return False
    except Exception as e:
        return False


if __name__ == '__main__':
    print("\n" + "="*60)
    print("API TOTVS(Eletrodata) - Agenda Técnica")
    print("="*60)
    
    if test_database_connection():
        print(" Banco de dados ok\n")
    else:
        print("Banco de dados indisponível\n")
    
    app = create_app()
    
    host = '0.0.0.0'
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    print("API TOTVS(Eletrodata) - Agenda Técnica")
    print(f"http://0.0.0.0:{port}")
    print(f"http://0.0.0.0:{port}/health")
    print("\nConsultas disponíveis:")
    print("   planilha_importacao, admitidos_demitidos,")
    print("   realocados, funcoes, cargos, tomadores")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
