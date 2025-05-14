"""
GUI - Interface gráfica do gerenciador Kanban
Design moderno com paleta de cores harmoniosa
"""
import customtkinter as ctk
from datetime import datetime
from decimal import Decimal, InvalidOperation
import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import subprocess
import sys
from typing import Dict, List, Optional
from models import Projeto, Etapa, Faturamento
from db import Database, DatabaseError


# PALETA DE CORES MODERNA - Baseada em Material Design
COLOR_PALETTE = {
    # Cores primárias
    'primary': '#2563EB',        # Azul moderno
    'primary_dark': '#1D4ED8',   # Azul escuro
    'primary_light': '#3B82F6',  # Azul claro
    
    # Cores de fundo
    'bg_primary': '#F8FAFC',     # Branco levemente acinzentado
    'bg_secondary': '#F1F5F9',   # Cinza muito claro
    'bg_tertiary': '#E2E8F0',    # Cinza claro
    
    # Cores de texto
    'text_primary': '#0F172A',   # Quase preto
    'text_secondary': '#475569', # Cinza escuro
    'text_muted': '#94A3B8',     # Cinza médio
    
    # Cores de status
    'success': '#10B981',        # Verde
    'warning': '#F59E0B',        # Laranja
    'danger': '#EF4444',         # Vermelho
    'info': '#06B6D4',           # Ciano
    
    # Cores específicas do Kanban
    'card_bg': '#FFFFFF',        # Branco puro para cards
    'card_border': '#E2E8F0',    # Borda sutil dos cards
    'column_bg': '#F8FAFC',      # Fundo das colunas
    
    # Cores hover
    'hover_light': '#F1F5F9',    # Hover claro
    'hover_primary': '#1E40AF',  # Hover do primary
}

# Configurações do tema CustomTkinter
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")


class ProjetoCard(ctk.CTkFrame):
    """Widget para exibir um cartão de projeto com design moderno"""
    
    def __init__(self, parent, projeto: Projeto, etapas: List[Etapa], on_update_callback, database: Database):
        super().__init__(
            parent, 
            corner_radius=12,
            border_width=1,
            border_color=COLOR_PALETTE['card_border'],
            fg_color=COLOR_PALETTE['card_bg']
        )
        
        if database is None:
            raise ValueError("Database não foi fornecido para ProjetoCard")
        
        self.projeto = projeto
        self.etapas = etapas
        self.on_update_callback = on_update_callback
        self.database = database
        
        self._create_widgets()
        self._setup_layout()
        
        # Efeito hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Efeito hover ao passar o mouse"""
        self.configure(border_color=COLOR_PALETTE['primary_light'])
    
    def _on_leave(self, event):
        """Remove o efeito hover"""
        self.configure(border_color=COLOR_PALETTE['card_border'])
    
    def _create_widgets(self):
        """Cria os widgets do cartão com design moderno"""
        # Título do projeto
        self.titulo = ctk.CTkLabel(
            self, 
            text=self.projeto.nome,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLOR_PALETTE['text_primary'],
            wraplength=250
        )
        
        # Receita total com destaque
        receita_text = f"R$ {self.projeto.receita_total:,.2f}"
        self.receita = ctk.CTkLabel(
            self, 
            text=receita_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_PALETTE['success']
        )
        
        # Etapa atual com cor suave
        etapa_atual = next((e.nome for e in self.etapas if e.id == self.projeto.etapa_atual), "Desconhecida")
        self.etapa = ctk.CTkLabel(
            self, 
            text=f"📍 {etapa_atual}",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_PALETTE['text_muted']
        )
        
        # Container para botões
        self.btn_container = ctk.CTkFrame(self, fg_color="transparent")
        
        # Botão abrir no VS Code
        self.btn_abrir_vs = ctk.CTkButton(
            self.btn_container,
            text="🎯 Abrir VS Code",
            command=self._abrir_no_vscode,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_PALETTE['primary'],
            hover_color=COLOR_PALETTE['primary_dark'],
            corner_radius=8
        )
        
        # Botão adicionar receita
        self.btn_receita = ctk.CTkButton(
            self.btn_container,
            text="💰 + Receita",
            command=self._adicionar_receita,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_PALETTE['success'],
            hover_color="#059669",
            corner_radius=8
        )
        
        # Frame para botões secundários
        self.btn_secondary = ctk.CTkFrame(self.btn_container, fg_color="transparent")
        
        # Botão editar projeto
        self.btn_editar = ctk.CTkButton(
            self.btn_secondary,
            text="✏️ Editar",
            command=self._editar_projeto,
            height=32,
            width=80,
            font=ctk.CTkFont(size=12),
            fg_color=COLOR_PALETTE['info'],
            hover_color="#0891B2",
            corner_radius=6
        )
        
        # Botão voltar etapa
        self.btn_voltar = ctk.CTkButton(
            self.btn_secondary,
            text="⬅️",
            command=self._voltar_projeto,
            height=32,
            width=45,
            font=ctk.CTkFont(size=12),
            fg_color=COLOR_PALETTE['warning'],
            hover_color="#D97706",
            corner_radius=6
        )
        
        # Botão avançar etapa
        self.btn_avancar = ctk.CTkButton(
            self.btn_secondary,
            text="➡️",
            command=self._avancar_projeto,
            height=32,
            width=45,
            font=ctk.CTkFont(size=12),
            fg_color=COLOR_PALETTE['warning'],
            hover_color="#D97706",
            corner_radius=6
        )
    
    def _setup_layout(self):
        """Organiza o layout com espaçamentos modernos"""
        # Configuração de grid com padding interno
        self.grid_columnconfigure(0, weight=1)
        
        # Título com destaque
        self.titulo.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        
        # Receita com espaçamento menor
        self.receita.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        
        # Etapa com espaçamento menor
        self.etapa.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
        
        # Container de botões
        self.btn_container.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 16))
        self.btn_container.grid_columnconfigure(0, weight=1)
        
        # Botões principais com espaçamento
        self.btn_abrir_vs.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.btn_receita.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        
        # Frame de botões secundários
        self.btn_secondary.grid(row=2, column=0, sticky="ew")
        self.btn_secondary.grid_columnconfigure(0, weight=1)
        self.btn_secondary.grid_columnconfigure(1, weight=0)
        self.btn_secondary.grid_columnconfigure(2, weight=0)
        
        # Botões secundários alinhados
        self.btn_editar.grid(row=0, column=0, sticky="w")
        self.btn_voltar.grid(row=0, column=1, sticky="e", padx=(8, 4))
        self.btn_avancar.grid(row=0, column=2, sticky="e", padx=(4, 0))
    
    def _abrir_no_vscode(self):
        """Abre o projeto no VS Code"""
        if not self.projeto.pasta_local:
            messagebox.showwarning("Aviso", "Pasta do projeto não definida!")
            return
        
        if not os.path.exists(self.projeto.pasta_local):
            messagebox.showerror("Erro", "Pasta do projeto não existe!")
            return
        
        try:
            if sys.platform == "win32":
                subprocess.run(["code", self.projeto.pasta_local], shell=True, check=True)
            else:
                subprocess.run(["code", self.projeto.pasta_local], check=True)
        except subprocess.CalledProcessError:
            try:
                if sys.platform == "win32":
                    subprocess.run(["devenv", self.projeto.pasta_local], shell=True, check=True)
                else:
                    subprocess.run(["xdg-open", self.projeto.pasta_local], check=True)
            except subprocess.CalledProcessError:
                messagebox.showerror("Erro", "Não foi possível abrir o editor. Verifique se o VS Code está instalado.")
    
    def _adicionar_receita(self):
        """Abre dialog para adicionar receita"""
        dialog = ReceitaDialog(self, self.projeto.id, self.database)
        self.wait_window(dialog.dialog)
        
        if dialog.resultado:
            self.on_update_callback()
    
    def _editar_projeto(self):
        """Abre dialog para editar projeto"""
        dialog = ProjetoDialog(self, self.database, self.projeto)
        self.wait_window(dialog.dialog)
        
        if dialog.resultado:
            self.on_update_callback()
    
    def _voltar_projeto(self):
        """Move o projeto para a etapa anterior"""
        etapas_ordenadas = sorted(self.etapas, key=lambda e: e.ordem)
        etapa_atual_idx = next((i for i, e in enumerate(etapas_ordenadas) 
                               if e.id == self.projeto.etapa_atual), 0)
        
        if etapa_atual_idx > 0:
            nova_etapa = etapas_ordenadas[etapa_atual_idx - 1]
            self.on_update_callback("mover_projeto", {
                "projeto_id": self.projeto.id,
                "nova_etapa": nova_etapa.id
            })
        else:
            messagebox.showinfo("Info", "Projeto já está na primeira etapa!")
    
    def _avancar_projeto(self):
        """Move o projeto para a próxima etapa"""
        etapas_ordenadas = sorted(self.etapas, key=lambda e: e.ordem)
        etapa_atual_idx = next((i for i, e in enumerate(etapas_ordenadas) 
                               if e.id == self.projeto.etapa_atual), 0)
        
        if etapa_atual_idx < len(etapas_ordenadas) - 1:
            nova_etapa = etapas_ordenadas[etapa_atual_idx + 1]
            self.on_update_callback("mover_projeto", {
                "projeto_id": self.projeto.id,
                "nova_etapa": nova_etapa.id
            })
        else:
            messagebox.showinfo("Info", "Projeto já está na última etapa!")
    
    def atualizar_dados(self, projeto: Projeto):
        """Atualiza os dados exibidos no cartão"""
        self.projeto = projeto
        self.titulo.configure(text=projeto.nome)
        self.receita.configure(text=f"R$ {projeto.receita_total:,.2f}")
        
        etapa_atual = next((e.nome for e in self.etapas if e.id == projeto.etapa_atual), "Desconhecida")
        self.etapa.configure(text=f"📍 {etapa_atual}")


class ReceitaDialog:
    """Dialog moderno para adicionar receita"""
    
    def __init__(self, parent, projeto_id: int, database: Database):
        self.parent = parent
        self.projeto_id = projeto_id
        self.database = database
        self.resultado = None
        
        # Cria o dialog com design moderno
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Nova Receita")
        self.dialog.geometry("450x380")
        self.dialog.resizable(False, False)
        
        # Configuração de aparência
        self.dialog.configure(fg_color=COLOR_PALETTE['bg_primary'])
        
        # Centraliza o dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Cria os widgets do dialog com design moderno"""
        # Container principal
        self.main_frame = ctk.CTkFrame(
            self.dialog,
            corner_radius=16,
            fg_color=COLOR_PALETTE['card_bg'],
            border_width=1,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Título com ícone
        self.titulo = ctk.CTkLabel(
            self.main_frame,
            text="💰 Nova Receita",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_PALETTE['text_primary']
        )
        
        # Campo valor
        self.valor_label = ctk.CTkLabel(
            self.main_frame,
            text="Valor (R$)",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_PALETTE['text_secondary']
        )
        self.valor_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="0.00",
            width=280,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Campo data
        self.data_label = ctk.CTkLabel(
            self.main_frame,
            text="Data",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_PALETTE['text_secondary']
        )
        self.data_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text=datetime.now().strftime("%Y-%m-%d"),
            width=280,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Campo descrição
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Descrição (opcional)",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_PALETTE['text_secondary']
        )
        self.desc_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Descrição da receita",
            width=280,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Frame para botões
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        # Botões com cores diferenciadas
        self.btn_salvar = ctk.CTkButton(
            self.btn_frame,
            text="✅ Salvar",
            command=self._salvar_receita,
            width=130,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_PALETTE['success'],
            hover_color="#059669",
            corner_radius=8
        )
        self.btn_cancelar = ctk.CTkButton(
            self.btn_frame,
            text="❌ Cancelar",
            command=self._cancelar,
            width=130,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_PALETTE['danger'],
            hover_color="#DC2626",
            corner_radius=8
        )
    
    def _setup_layout(self):
        """Organiza o layout com espaçamentos modernos"""
        # Container principal
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Elementos com espaçamento consistente
        self.titulo.grid(row=0, column=0, pady=(20, 30))
        
        self.valor_label.grid(row=1, column=0, sticky="w", padx=30, pady=(0, 5))
        self.valor_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.data_label.grid(row=3, column=0, sticky="w", padx=30, pady=(0, 5))
        self.data_entry.grid(row=4, column=0, padx=30, pady=(0, 15))
        
        self.desc_label.grid(row=5, column=0, sticky="w", padx=30, pady=(0, 5))
        self.desc_entry.grid(row=6, column=0, padx=30, pady=(0, 25))
        
        # Frame dos botões
        self.btn_frame.grid(row=7, column=0, pady=(0, 20))
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        
        # Botões com espaçamento
        self.btn_salvar.grid(row=0, column=0, padx=(0, 10))
        self.btn_cancelar.grid(row=0, column=1, padx=(10, 0))
        
        # Foco inicial
        self.valor_entry.focus_set()
        self.dialog.update_idletasks()
    
    def _salvar_receita(self):
        """Salva a receita no banco de dados"""
        # Validação dos campos
        try:
            valor_str = self.valor_entry.get().strip()
            valor = Decimal(valor_str.replace(',', '.'))
            if valor <= 0:
                raise ValueError("Valor deve ser positivo")
        except (ValueError, InvalidOperation):
            messagebox.showerror("Erro", "Valor inválido! Use formato: 123.45")
            return
        
        try:
            data_str = self.data_entry.get().strip()
            if not data_str:
                data_str = datetime.now().strftime("%Y-%m-%d")
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Use formato: YYYY-MM-DD")
            return
        
        descricao = self.desc_entry.get().strip() or None
        
        # Cria o faturamento
        faturamento = Faturamento(
            id=None,
            projeto_id=self.projeto_id,
            valor=valor,
            descricao=descricao,
            data_faturamento=data
        )
        
        # Salva no banco
        try:
            self.database.adicionar_faturamento(faturamento)
            self.resultado = faturamento
            self.dialog.destroy()
        except DatabaseError as e:
            messagebox.showerror("Erro", f"Erro ao salvar receita: {e}")
    
    def _cancelar(self):
        """Cancela a operação"""
        self.dialog.destroy()


class ProjetoDialog:
    """Dialog moderno para criar/editar projeto"""
    
    def __init__(self, parent, database: Database, projeto: Optional[Projeto] = None):
        self.parent = parent
        self.database = database
        self.projeto = projeto
        self.resultado = None
        self.editing = projeto is not None
        
        # Cria o dialog com design moderno
        self.dialog = ctk.CTkToplevel(parent)
        title = "Editar Projeto" if self.editing else "Novo Projeto"
        self.dialog.title(title)
        self.dialog.geometry("550x600")
        self.dialog.resizable(False, False)
        
        # Configuração de aparência
        self.dialog.configure(fg_color=COLOR_PALETTE['bg_primary'])
        
        # Centraliza o dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._setup_layout()
        self._load_data()
    
    def _create_widgets(self):
        """Cria os widgets do dialog com design moderno"""
        # Container principal
        self.main_frame = ctk.CTkFrame(
            self.dialog,
            corner_radius=16,
            fg_color=COLOR_PALETTE['card_bg'],
            border_width=1,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Título com ícone
        title_text = "✏️ Editar Projeto" if self.editing else "➕ Novo Projeto"
        self.titulo = ctk.CTkLabel(
            self.main_frame,
            text=title_text,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_PALETTE['text_primary']
        )
        
        # Campo nome
        self.nome_label = ctk.CTkLabel(
            self.main_frame,
            text="Nome do Projeto",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_PALETTE['text_secondary']
        )
        self.nome_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Nome do projeto",
            width=320,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Campo descrição
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Descrição",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_PALETTE['text_secondary']
        )
        self.desc_entry = ctk.CTkTextbox(
            self.main_frame,
            width=320,
            height=90,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Campo pasta local
        self.pasta_label = ctk.CTkLabel(
            self.main_frame,
            text="Pasta Local",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_PALETTE['text_secondary']
        )
        self.pasta_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pasta_entry = ctk.CTkEntry(
            self.pasta_frame,
            placeholder_text="Caminho para a pasta",
            width=230,
            height=40,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            border_color=COLOR_PALETTE['card_border']
        )
        self.pasta_btn = ctk.CTkButton(
            self.pasta_frame,
            text="📁",
            command=self._procurar_pasta,
            width=60,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_PALETTE['info'],
            hover_color="#0891B2",
            corner_radius=8
        )
        
        # Campo arquivo principal
        self.arquivo_label = ctk.CTkLabel(
            self.main_frame,
            text="Arquivo Principal",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_PALETTE['text_secondary']
        )
        self.arquivo_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="arquivo.py, index.html, etc.",
            width=320,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Frame para botões
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        # Botões principais
        self.btn_salvar = ctk.CTkButton(
            self.btn_frame,
            text="✅ Salvar",
            command=self._salvar_projeto,
            width=130,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_PALETTE['success'],
            hover_color="#059669",
            corner_radius=8
        )
        self.btn_cancelar = ctk.CTkButton(
            self.btn_frame,
            text="❌ Cancelar",
            command=self._cancelar,
            width=130,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_PALETTE['danger'],
            hover_color="#DC2626",
            corner_radius=8
        )
        
        # Botão excluir (apenas para edição)
        if self.editing:
            self.btn_excluir = ctk.CTkButton(
                self.btn_frame,
                text="🗑️ Excluir",
                command=self._excluir_projeto,
                width=130,
                height=40,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COLOR_PALETTE['danger'],
                hover_color="#DC2626",
                corner_radius=8
            )
    
    def _setup_layout(self):
        """Organiza o layout com espaçamentos modernos"""
        # Container principal
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Elementos com espaçamento consistente
        self.titulo.grid(row=0, column=0, pady=(20, 30))
        
        self.nome_label.grid(row=1, column=0, sticky="w", padx=30, pady=(0, 5))
        self.nome_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.desc_label.grid(row=3, column=0, sticky="w", padx=30, pady=(0, 5))
        self.desc_entry.grid(row=4, column=0, padx=30, pady=(0, 15))
        
        # Pasta local com botão
        self.pasta_label.grid(row=5, column=0, sticky="w", padx=30, pady=(0, 5))
        self.pasta_frame.grid(row=6, column=0, padx=30, pady=(0, 15))
        self.pasta_frame.grid_columnconfigure(0, weight=1)
        self.pasta_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.pasta_btn.grid(row=0, column=1)
        
        self.arquivo_label.grid(row=7, column=0, sticky="w", padx=30, pady=(0, 5))
        self.arquivo_entry.grid(row=8, column=0, padx=30, pady=(0, 25))
        
        # Frame dos botões
        self.btn_frame.grid(row=9, column=0, pady=(0, 20))
        
        # Layout dos botões dependendo se é edição ou criação
        if self.editing:
            self.btn_frame.grid_columnconfigure(0, weight=1)
            self.btn_frame.grid_columnconfigure(1, weight=1)
            self.btn_frame.grid_columnconfigure(2, weight=1)
            
            self.btn_salvar.grid(row=0, column=0, padx=(0, 5))
            self.btn_excluir.grid(row=0, column=1, padx=5)
            self.btn_cancelar.grid(row=0, column=2, padx=(5, 0))
        else:
            self.btn_frame.grid_columnconfigure(0, weight=1)
            self.btn_frame.grid_columnconfigure(1, weight=1)
            
            self.btn_salvar.grid(row=0, column=0, padx=(0, 10))
            self.btn_cancelar.grid(row=0, column=1, padx=(10, 0))
        
        # Foco inicial
        self.nome_entry.focus_set()
        self.dialog.update_idletasks()
    
    def _load_data(self):
        """Carrega os dados do projeto para edição"""
        if self.projeto:
            self.nome_entry.insert(0, self.projeto.nome)
            self.desc_entry.insert("1.0", self.projeto.descricao or "")
            self.pasta_entry.insert(0, self.projeto.pasta_local or "")
            self.arquivo_entry.insert(0, self.projeto.arquivo_principal or "")
    
    def _procurar_pasta(self):
        """Abre dialog para selecionar pasta"""
        from tkinter import filedialog
        pasta = filedialog.askdirectory(title="Selecionar Pasta do Projeto")
        if pasta:
            self.pasta_entry.delete(0, "end")
            self.pasta_entry.insert(0, pasta)
    
    def _salvar_projeto(self):
        """Salva/atualiza o projeto"""
        # Validação
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome do projeto é obrigatório!")
            return
        
        # Dados do projeto
        descricao = self.desc_entry.get("1.0", "end-1c").strip() or None
        pasta_local = self.pasta_entry.get().strip() or None
        arquivo_principal = self.arquivo_entry.get().strip() or None
        
        try:
            if self.editing:
                # Atualiza projeto existente
                self.projeto.nome = nome
                self.projeto.descricao = descricao
                self.projeto.pasta_local = pasta_local
                self.projeto.arquivo_principal = arquivo_principal
                self.database.atualizar_projeto(self.projeto)
                self.resultado = self.projeto
            else:
                # Cria novo projeto
                projeto = Projeto(
                    id=None, nome=nome, descricao=descricao,
                    pasta_local=pasta_local, arquivo_principal=arquivo_principal,
                    etapa_atual=1  # Backlog por padrão
                )
                projeto_id = self.database.criar_projeto(projeto)
                projeto.id = projeto_id
                self.resultado = projeto
            
            self.dialog.destroy()
        except DatabaseError as e:
            messagebox.showerror("Erro", f"Erro ao salvar projeto: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
    
    def _excluir_projeto(self):
        """Exclui o projeto"""
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este projeto?"):
            try:
                self.database.excluir_projeto(self.projeto.id)
                self.resultado = "excluido"
                self.dialog.destroy()
            except DatabaseError as e:
                messagebox.showerror("Erro", f"Erro ao excluir projeto: {e}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado: {e}")
    
    def _cancelar(self):
        """Cancela a operação"""
        self.dialog.destroy()


class KanbanColumn(ctk.CTkFrame):
    """Coluna do Kanban com design moderno"""
    
    def __init__(self, parent, etapa: Etapa, etapas: List[Etapa], on_update_callback, database: Database):
        super().__init__(
            parent, 
            corner_radius=12,
            border_width=1,
            border_color=COLOR_PALETTE['card_border'],
            fg_color=COLOR_PALETTE['column_bg']
        )
        
        # Armazena todas as propriedades necessárias
        self.etapa = etapa
        self.etapas = etapas
        self.on_update_callback = on_update_callback
        self.database = database
        self.cards: List[ProjetoCard] = []
        
        if self.database is None:
            raise ValueError(f"Database não foi fornecido para coluna {etapa.nome}")
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Cria os widgets da coluna com design moderno"""
        # Cabeçalho da coluna com ícones
        icons = {
            'Backlog': '📋',
            'Em Andamento': '⚡',
            'Em Revisão': '🔍',
            'Concluído': '✅'
        }
        icon = icons.get(self.etapa.nome, '📌')
        
        self.header = ctk.CTkLabel(
            self,
            text=f"{icon} {self.etapa.nome}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_PALETTE['text_primary'],
            height=50
        )
        
        # Frame scrollable para os cartões com design moderno
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=300,
            height=600,
            corner_radius=8,
            fg_color=COLOR_PALETTE['bg_secondary'],
            border_width=1,
            border_color=COLOR_PALETTE['card_border']
        )
    
    def _setup_layout(self):
        """Organiza o layout com espaçamentos modernos"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header com padding
        self.header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        
        # Frame scrollable com padding
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
    
    def adicionar_projeto(self, projeto: Projeto):
        """Adiciona um projeto à coluna"""
        try:
            if self.database is None:
                raise ValueError(f"Database é None na coluna {self.etapa.nome}")
            
            # Cria o card com espaçamento moderno
            card = ProjetoCard(
                self.scrollable_frame,
                projeto,
                self.etapas,
                self.on_update_callback,
                self.database
            )
            
            # Grid com espaçamento entre cards
            card.grid(row=len(self.cards), column=0, sticky="ew", padx=8, pady=8)
            self.cards.append(card)
            
        except Exception as e:
            print(f"ERRO ao adicionar projeto '{projeto.nome}': {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao adicionar projeto: {e}")
    
    def remover_projeto(self, projeto_id: int):
        """Remove um projeto da coluna"""
        for i, card in enumerate(self.cards):
            if card.projeto.id == projeto_id:
                card.destroy()
                self.cards.pop(i)
                # Reorganiza os cartões restantes
                for j, remaining_card in enumerate(self.cards[i:], start=i):
                    remaining_card.grid_forget()
                    remaining_card.grid(row=j, column=0, sticky="ew", padx=8, pady=8)
                break
    
    def atualizar_projeto(self, projeto: Projeto):
        """Atualiza um projeto específico na coluna"""
        for card in self.cards:
            if card.projeto.id == projeto.id:
                card.atualizar_dados(projeto)
                break
    
    def limpar(self):
        """Remove todos os cartões da coluna"""
        for card in self.cards:
            card.destroy()
        self.cards.clear()


class KanbanGUI:
    """Interface principal do sistema Kanban com design moderno"""
    
    def __init__(self, database: Database):
        self.db = database
        self.db.add_observer(self)
        
        # Configuração da janela principal
        self.root = ctk.CTk()
        self.root.title("🔧 Kanban Projects Manager")
        self.root.geometry("1400x800")
        self.root.state('zoomed')
        
        # Configura a cor de fundo da janela
        self.root.configure(fg_color=COLOR_PALETTE['bg_primary'])
        
        self.etapas: List[Etapa] = []
        self.colunas: Dict[int, KanbanColumn] = {}
        
        self._create_widgets()
        self._setup_layout()
        self._load_initial_data()
    
    def _create_widgets(self):
        """Cria os widgets principais com design moderno"""
        # Header com design elegante
        self.header_frame = ctk.CTkFrame(
            self.root,
            height=90,
            corner_radius=16,
            fg_color=COLOR_PALETTE['card_bg'],
            border_width=1,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Título com ícone e fonte moderna
        self.title = ctk.CTkLabel(
            self.header_frame,
            text="🔧 Kanban Projects Manager",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLOR_PALETTE['primary']
        )
        
        # Subtítulo
        self.subtitle = ctk.CTkLabel(
            self.header_frame,
            text="Gerencie seus projetos com eficiência",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_PALETTE['text_muted']
        )
        
        # Botão novo projeto com design destacado
        self.btn_novo_projeto = ctk.CTkButton(
            self.header_frame,
            text="➕ Novo Projeto",
            command=self._novo_projeto,
            width=180,
            height=50,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_PALETTE['primary'],
            hover_color=COLOR_PALETTE['primary_dark'],
            corner_radius=12
        )
        
        # Frame principal para as colunas
        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=16,
            fg_color=COLOR_PALETTE['bg_secondary'],
            border_width=1,
            border_color=COLOR_PALETTE['card_border']
        )
        
        # Frame scrollable para as colunas do Kanban
        self.kanban_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            orientation="horizontal",
            height=700,
            fg_color="transparent"
        )
    
    def _setup_layout(self):
        """Organiza o layout com espaçamentos modernos"""
        # Configura o grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header com padding elegante
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Layout do header
        self.title.grid(row=0, column=0, sticky="w", padx=30, pady=(20, 5))
        self.subtitle.grid(row=1, column=0, sticky="w", padx=30, pady=(0, 20))
        self.btn_novo_projeto.grid(row=0, column=2, rowspan=2, padx=30, pady=20)
        
        # Main frame
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Kanban frame
        self.kanban_frame.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
    
    def _load_initial_data(self):
        """Carrega os dados iniciais do banco"""
        try:
            print("🚀 Carregando dados iniciais...")
            
            # Carrega as etapas
            self.etapas = self.db.get_etapas()
            print(f"✓ {len(self.etapas)} etapas carregadas")
            
            # Cria as colunas do Kanban com espaçamento moderno
            for etapa in self.etapas:
                coluna = KanbanColumn(
                    self.kanban_frame, etapa, self.etapas,
                    self._handle_update_callback, self.db
                )
                coluna.grid(row=0, column=etapa.ordem-1, sticky="ns", padx=8, pady=8)
                self.colunas[etapa.id] = coluna
            
            # Carrega os projetos
            self._load_projetos()
            
        except DatabaseError as e:
            print(f"❌ Erro de database: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
    
    def _load_projetos(self):
        """Carrega todos os projetos nas colunas apropriadas"""
        try:
            # Limpa as colunas
            for coluna in self.colunas.values():
                coluna.limpar()
            
            # Carrega os projetos
            projetos = self.db.get_projetos()
            print(f"✓ {len(projetos)} projetos carregados")
            
            # Adiciona cada projeto à coluna correspondente
            for projeto in projetos:
                if projeto.etapa_atual in self.colunas:
                    self.colunas[projeto.etapa_atual].adicionar_projeto(projeto)
                else:
                    print(f"⚠️ Projeto {projeto.nome} tem etapa inválida: {projeto.etapa_atual}")
                    
        except DatabaseError as e:
            messagebox.showerror("Erro", f"Erro ao carregar projetos: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado ao carregar projetos: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
    
    def _novo_projeto(self):
        """Abre dialog para criar novo projeto"""
        try:
            dialog = ProjetoDialog(self.root, self.db)
            self.root.wait_window(dialog.dialog)
            
            if dialog.resultado:
                print(f"✓ Projeto '{dialog.resultado.nome}' criado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao criar projeto: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao criar projeto: {e}")
    
    def _handle_update_callback(self, action=None, data=None):
        """Manipula callbacks de atualização dos cartões"""
        if action == "mover_projeto":
            try:
                self.db.mover_projeto_etapa(data["projeto_id"], data["nova_etapa"])
                self._load_projetos()
            except DatabaseError as e:
                print(f"❌ Erro ao mover projeto: {e}")
                messagebox.showerror("Erro", f"Erro ao mover projeto: {e}")
        else:
            self._load_projetos()
    
    def update(self, event: str, data: dict = None):
        """Implementação do Observer - reage a mudanças no banco"""
        # Recarrega os projetos quando houver mudanças
        if event in ["projeto_criado", "projeto_atualizado", "projeto_movido", 
                     "projeto_excluido", "faturamento_adicionado", "faturamento_excluido"]:
            self._load_projetos()
    
    def run(self):
        """Inicia a aplicação"""
        try:
            self.root.mainloop()
        finally:
            self.db.close()