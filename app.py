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
            logger.info(" banco de dados OK")
            return True
        else:
            logger.error("Erro ao conectar ao banco de dados")
            return False
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
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
    
    print("\n" + "="*60)
    print("API TOTVS(Eletrodata) - Agenda Técnica")
    print("="*60)
    print(f"🌐 http://0.0.0.0:{port}")
    print(f"💚 Health: http://0.0.0.0:{port}/health")
    print("\n📋 Consultas disponíveis:")
    print("   planilha_importacao, admitidos_demitidos,")
    print("   realocados, funcoes, cargos, tomadores")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
