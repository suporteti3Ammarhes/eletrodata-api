import pymssql
import pandas as pd
import logging
from typing import Optional, List, Any, Dict
from contextlib import contextmanager
import os

try:
    from config.settings import DATABASE_CONFIG
except ImportError:
    DATABASE_CONFIG = {
        'server': '147.79.83.7',
        'database': 'agendaHomologacao',
        'username': 'sa',
        'password': 'A7qmhn6vO9RxpRzwGE7AhR2ZkEfEPUHtOWBxuNaCydZGljv6CgfftIj6vfO',
        'port': 1433,
        'timeout': 30
    }

class DatabaseService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._connection = None
        ## EVITA PROBLEMAS.
        self.campo_limits = {
            'nome': 500,
            'funcao': 500,
            'nome1': 500,
            'setor': 500,
            'subsetor': 500,
            'status': 50,
            'chapa': 50,
            'cpf': 50,
            'pispasep': 50,
            'codcargo': 50,
            'codfuncao': 50,
            'cbo': 50,
            'codccusto': 50,
            'dtnascimento': 50,
            'dataadmissao': 50
        }
    
    @contextmanager
    def get_connection(self):
        connection = None
        try:
            self.logger.info("Connecting to database...")
            connection = pymssql.connect(
                server=DATABASE_CONFIG['server'],
                user=DATABASE_CONFIG['username'],
                password=DATABASE_CONFIG['password'],
                database=DATABASE_CONFIG['database'],
                port=DATABASE_CONFIG['port'],
                timeout=DATABASE_CONFIG['timeout']
            )
            self.logger.info("Database connection established successfully")
            yield connection
        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            raise
        finally:
            if connection:
                connection.close()
                self.logger.info("Database connection closed")
    
    def test_connection(self) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
                return result[0] == 1
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def execute_query(self, query: str) -> Optional[List[Dict[str, Any]]]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                
                columns = [column[0] for column in cursor.description]
                
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    results.append(dict(zip(columns, row)))
                
                self.logger.info(f"Query executed successfully. {len(results)} records found")
                return results
                
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            return None
    
    def execute_query_to_dataframe(self, query: str) -> Optional[pd.DataFrame]:
        try:
            with self.get_connection() as conn:
                df = pd.read_sql(query, conn)
                self.logger.info(f"Query executed successfully. DataFrame created with {len(df)} records")
                return df
        except Exception as e:
            self.logger.error(f"Error executing DataFrame query: {e}")
            return None
    
    def insert_batch(self, table: str, records: List[Dict[str, Any]]) -> bool:
        """Essa funcao, facilita para INSERCAO DE MUITOS VALORES DE UMA VEZ só , puxa do config.py os campos e os valores são passados de acordo com a API da eletrodata, isso para podermos facilitar a insercao no banco de dados"""
        if not records:
            self.logger.warning("No records to insert")
            return True
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for idx, record in enumerate(records):
                    try:
                        registro_limpo = self._limpar_registro(record)
                        
                        colunas = ', '.join(f'[{col}]' for col in registro_limpo.keys())
                        placeholders = ', '.join(['%s'] * len(registro_limpo))
                        query = f"INSERT INTO [{table}] ({colunas}) VALUES ({placeholders})"
                        valores = tuple(registro_limpo.values())
                        
                        cursor.execute(query, valores)
                    except Exception as e:
                        self.logger.error(f"Erro no registro #{idx}: {record}")
                        self.logger.error(f"Registro limpo: {registro_limpo}")
                        raise
                
                conn.commit()
                self.logger.info(f"{len(records)} registros inseridos em {table}")
                return True
                
        except Exception as e:
            self.logger.error(f"Erro ao inserir em {table}: {e}")
            return False
    
    def _limpar_registro(self, registro: Dict[str, Any]) -> Dict[str, Any]:
       
        registro_limpo = {}
        
        for chave, valor in registro.items():
            if isinstance(valor, str):
                valor = valor.strip().replace('\n', '').replace('\r', '')
                valor = ' '.join(valor.split())
                
                max_length = self.campo_limits.get(chave, 500)
                if len(valor) > max_length:
                  """por algum motivo, tava dando muito ERRO, por passar da capacidade """
                  self.logger.warning(f"Campo '{chave}' truncado de {len(valor)} para {max_length} caracteres")
                  valor = valor[:max_length]
                
                valor = valor if valor else None
            
            registro_limpo[chave] = valor
        
        return registro_limpo
