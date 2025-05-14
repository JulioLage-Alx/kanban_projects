"""
Database - Camada de acesso aos dados MySQL
"""
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
import os
from models import Projeto, Etapa, Faturamento, Observable


class DatabaseError(Exception):
    """Exceção personalizada para erros de banco de dados"""
    pass


class Database(Observable):
    """Classe para gerenciar conexões e operações do MySQL"""
    
    def __init__(self, host='localhost', user='root', password='', database='kanban_projects'):
        super().__init__()
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True
        }
        self.connection = None
        self._connect()
    
    def _connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("✓ Conexão com MySQL estabelecida")
        except Error as e:
            raise DatabaseError(f"Erro ao conectar com MySQL: {e}")
    
    def _ensure_connection(self):
        """Garante que a conexão está ativa"""
        if not self.connection or not self.connection.is_connected():
            self._connect()
    
    def execute_script(self, script_path: str):
        """Executa um script SQL"""
        self._ensure_connection()
        try:
            with open(script_path, 'r', encoding='utf-8') as file:
                script = file.read()
            
            cursor = self.connection.cursor()
            # Executa cada comando separadamente
            for statement in script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            cursor.close()
            print("✓ Script SQL executado com sucesso")
        except Exception as e:
            raise DatabaseError(f"Erro ao executar script: {e}")
    
    def get_etapas(self) -> List[Etapa]:
        """Retorna todas as etapas ordenadas"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nome, ordem FROM etapas ORDER BY ordem")
            etapas = [Etapa(*row) for row in cursor.fetchall()]
            cursor.close()
            return etapas
        except Error as e:
            raise DatabaseError(f"Erro ao buscar etapas: {e}")
    
    def get_etapa_by_id(self, etapa_id: int) -> Optional[Etapa]:
        """Retorna uma etapa específica"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nome, ordem FROM etapas WHERE id = %s", (etapa_id,))
            row = cursor.fetchone()
            cursor.close()
            return Etapa(*row) if row else None
        except Error as e:
            raise DatabaseError(f"Erro ao buscar etapa: {e}")
    
    def get_projetos(self) -> List[Projeto]:
        """Retorna todos os projetos com receita total"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT p.id, p.nome, p.descricao, p.pasta_local, p.arquivo_principal,
                       p.etapa_atual, p.data_criacao, p.data_atualizacao,
                       COALESCE(v.receita_total, 0) as receita_total
                FROM projetos p
                LEFT JOIN view_receita_projetos v ON p.id = v.id
                ORDER BY p.data_atualizacao DESC
            """
            cursor.execute(query)
            projetos = []
            for row in cursor.fetchall():
                projeto = Projeto(
                    id=row[0], nome=row[1], descricao=row[2],
                    pasta_local=row[3], arquivo_principal=row[4],
                    etapa_atual=row[5], data_criacao=row[6],
                    data_atualizacao=row[7], receita_total=Decimal(str(row[8]))
                )
                projetos.append(projeto)
            cursor.close()
            return projetos
        except Error as e:
            raise DatabaseError(f"Erro ao buscar projetos: {e}")
    
    def get_projeto_by_id(self, projeto_id: int) -> Optional[Projeto]:
        """Retorna um projeto específico"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT p.id, p.nome, p.descricao, p.pasta_local, p.arquivo_principal,
                       p.etapa_atual, p.data_criacao, p.data_atualizacao,
                       COALESCE(v.receita_total, 0) as receita_total
                FROM projetos p
                LEFT JOIN view_receita_projetos v ON p.id = v.id
                WHERE p.id = %s
            """
            cursor.execute(query, (projeto_id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Projeto(
                    id=row[0], nome=row[1], descricao=row[2],
                    pasta_local=row[3], arquivo_principal=row[4],
                    etapa_atual=row[5], data_criacao=row[6],
                    data_atualizacao=row[7], receita_total=Decimal(str(row[8]))
                )
            return None
        except Error as e:
            raise DatabaseError(f"Erro ao buscar projeto: {e}")
    
    def criar_projeto(self, projeto: Projeto) -> int:
        """Cria um novo projeto e retorna o ID"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO projetos (nome, descricao, pasta_local, arquivo_principal, etapa_atual)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (projeto.nome, projeto.descricao, projeto.pasta_local,
                     projeto.arquivo_principal, projeto.etapa_atual)
            cursor.execute(query, values)
            projeto_id = cursor.lastrowid
            cursor.close()
            
            self.notify("projeto_criado", {"projeto_id": projeto_id})
            return projeto_id
        except Error as e:
            raise DatabaseError(f"Erro ao criar projeto: {e}")
    
    def atualizar_projeto(self, projeto: Projeto):
        """Atualiza um projeto existente"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE projetos 
                SET nome = %s, descricao = %s, pasta_local = %s, 
                    arquivo_principal = %s, etapa_atual = %s
                WHERE id = %s
            """
            values = (projeto.nome, projeto.descricao, projeto.pasta_local,
                     projeto.arquivo_principal, projeto.etapa_atual, projeto.id)
            cursor.execute(query, values)
            cursor.close()
            
            self.notify("projeto_atualizado", {"projeto_id": projeto.id})
        except Error as e:
            raise DatabaseError(f"Erro ao atualizar projeto: {e}")
    
    def mover_projeto_etapa(self, projeto_id: int, nova_etapa: int):
        """Move um projeto para outra etapa"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = "UPDATE projetos SET etapa_atual = %s WHERE id = %s"
            cursor.execute(query, (nova_etapa, projeto_id))
            cursor.close()
            
            self.notify("projeto_movido", {
                "projeto_id": projeto_id, 
                "nova_etapa": nova_etapa
            })
        except Error as e:
            raise DatabaseError(f"Erro ao mover projeto: {e}")
    
    def excluir_projeto(self, projeto_id: int):
        """Exclui um projeto e seus faturamentos"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM projetos WHERE id = %s"
            cursor.execute(query, (projeto_id,))
            cursor.close()
            
            self.notify("projeto_excluido", {"projeto_id": projeto_id})
        except Error as e:
            raise DatabaseError(f"Erro ao excluir projeto: {e}")
    
    def get_faturamentos_projeto(self, projeto_id: int) -> List[Faturamento]:
        """Retorna todos os faturamentos de um projeto"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT id, projeto_id, valor, descricao, data_faturamento, data_criacao
                FROM faturamentos 
                WHERE projeto_id = %s 
                ORDER BY data_faturamento DESC
            """
            cursor.execute(query, (projeto_id,))
            faturamentos = [Faturamento(*row) for row in cursor.fetchall()]
            cursor.close()
            return faturamentos
        except Error as e:
            raise DatabaseError(f"Erro ao buscar faturamentos: {e}")
    
    def adicionar_faturamento(self, faturamento: Faturamento) -> int:
        """Adiciona um novo faturamento e retorna o ID"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO faturamentos (projeto_id, valor, descricao, data_faturamento)
                VALUES (%s, %s, %s, %s)
            """
            values = (faturamento.projeto_id, faturamento.valor,
                     faturamento.descricao, faturamento.data_faturamento)
            cursor.execute(query, values)
            faturamento_id = cursor.lastrowid
            cursor.close()
            
            self.notify("faturamento_adicionado", {
                "faturamento_id": faturamento_id,
                "projeto_id": faturamento.projeto_id
            })
            return faturamento_id
        except Error as e:
            raise DatabaseError(f"Erro ao adicionar faturamento: {e}")
    
    def excluir_faturamento(self, faturamento_id: int, projeto_id: int):
        """Exclui um faturamento"""
        self._ensure_connection()
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM faturamentos WHERE id = %s"
            cursor.execute(query, (faturamento_id,))
            cursor.close()
            
            self.notify("faturamento_excluido", {
                "faturamento_id": faturamento_id,
                "projeto_id": projeto_id
            })
        except Error as e:
            raise DatabaseError(f"Erro ao excluir faturamento: {e}")
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Conexão com MySQL fechada")