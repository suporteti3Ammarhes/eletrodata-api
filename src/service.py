from datetime import datetime
from .models import Consulta, ResultadoConsulta


class ConsultaService:
    
    def __init__(self, soap_client, consultas_config):
        self.soap_client = soap_client
        self.consultas_config = consultas_config
    
    def listar_consultas(self):
        return [{
            "nome": nome,
            "sentenca": cfg["sentenca"],
            "requer_periodo": cfg["requer_periodo"],
            "campos": cfg["campos"],
            "table": cfg.get("table", "")
        } for nome, cfg in self.consultas_config.items()]
    
    def executar_consulta(self, nome_consulta: str, mes: str = None, ano: int = None):
        config = self.consultas_config.get(nome_consulta)
        if not config:
            raise ValueError(f"Consulta '{nome_consulta}' não encontrada")
        
        consulta = Consulta(
            nome=nome_consulta,
            sentenca=config["sentenca"],
            parametros_fixos=config["parametros_fixos"],
            campos=config["campos"],
            requer_periodo=config["requer_periodo"],
            processar_status=config.get("processar_status", False),
            table=config.get("table", ""),
            campo_referencia=config.get("campo_referencia", "")
        )
        
        if consulta.requer_periodo and (not mes or not ano):
            raise ValueError(f"Consulta '{nome_consulta}' precisa de 'mes' e 'ano'")
        
        parametros = consulta.parametros_fixos
        if mes and ano:
            mes = str(int(mes)).zfill(2)
            parametros += f";MES={mes};ANO={ano}"
        
        dados = self.soap_client.executar(consulta, parametros)
        
        return ResultadoConsulta(
            consulta=consulta.nome,
            sentenca=consulta.sentenca,
            parametros=parametros,
            total_registros=len(dados),
            dados=dados,
            timestamp=datetime.now().isoformat()
        )
