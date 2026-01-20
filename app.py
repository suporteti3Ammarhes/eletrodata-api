import os
from src.app import create_app


if __name__ == '__main__':
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
