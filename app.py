from src.app import create_app


if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*60)
    print("API TOTVS(Eletrodata) - Agenda Técnica")
    print("="*60)
    print("🌐 http://localhost:5000")
    print("💚 http://localhost:5000/health")
    print("\n📋 Consultas disponíveis:")
    print("   planilha_importacao, admitidos_demitidos,")
    print("   realocados, funcoes, cargos, tomadores")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
