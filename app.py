from src.app import create_app


if __name__ == '__main__':
    app = create_app()
    
    host = '0.0.0.0'
    port = 5000
    
    print("\n" + "="*60)
    print("API TOTVS(Eletrodata) - Agenda Técnica")
    print("="*60)
    print(f"🌐 http://localhost:{port}")
    print(f"💚 Health: http://localhost:{port}/health")
    print("\n📋 Consultas disponíveis:")
    print("   planilha_importacao, admitidos_demitidos,")
    print("   realocados, funcoes, cargos, tomadores")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
