# 🔧 Kanban Projects Manager

Um sistema moderno de gerenciamento de projetos estilo Kanban com interface gráfica CustomTkinter, banco de dados MySQL e controle completo de faturamento.

## ✨ Recursos Principais

- **🎯 Interface Kanban Moderna** com 4 etapas (Backlog, Em Andamento, Em Revisão, Concluído)
- **💰 Controle de Faturamento** completo por projeto
- **🎯 Integração com VS Code** - Abre projetos diretamente no editor
- **🔄 Navegação Intuitiva** - Botões para mover projetos entre etapas
- **🎨 Design Moderno** com paleta de cores harmoniosa
- **📱 Interface Responsiva** com efeitos hover e feedback visual
- **🗄️ Banco MySQL** para persistência dos dados
- **🔄 Observer Pattern** para atualizações em tempo real

## 📸 Screenshots

<p align="center">
  <em>Interface principal do Kanban</em>
</p>

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **CustomTkinter** - Interface gráfica moderna
- **MySQL 5.7+** - Banco de dados
- **mysql-connector-python** - Conexão com MySQL
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📋 Pré-requisitos

- Python 3.8 ou superior
- MySQL 5.7+ ou superior
- VS Code (opcional, para abrir projetos)

## 🔧 Instalação

### 1. Clone ou baixe o projeto

```bash
git clone 
cd kanban-projects-manager
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados

#### 3.1. Crie o banco MySQL

O aplicativo criará automaticamente o banco de dados na primeira execução. Você apenas precisa ter o MySQL rodando.

#### 3.2. Configure as credenciais (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=kanban_projects
```

Ou configure diretamente no código editando `main.py`:

```python
def get_database_config():
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'sua_senha',
        'database': 'kanban_projects'
    }
```

### 4. Execute a aplicação

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
kanban-projects-manager/
├── main.py              # Inicialização da aplicação
├── models.py            # Classes de domínio (Projeto, Etapa, Faturamento)
├── db.py                # Camada de acesso ao banco de dados
├── gui.py               # Interface gráfica com CustomTkinter
├── setup_db.py          # Utilitário para configuração do banco
├── requirements.txt     # Dependências do Python
├── README.md           # Esta documentação
├── run.sh              # Script de execução (Linux/Mac)
├── run.bat             # Script de execução (Windows)
└── .env               # Configurações do banco (opcional)
```

## 🎯 Como Usar

### 🆕 Criando um Novo Projeto

1. Clique no botão **"➕ Novo Projeto"**
2. Preencha as informações:
   - **Nome**: Título do projeto
   - **Descrição**: Detalhes opcionais do projeto
   - **Pasta Local**: Caminho para o diretório do projeto
   - **Arquivo Principal**: Arquivo a ser aberto (ex: main.py, index.html)
3. Clique em **"✅ Salvar"**

### 💰 Adicionando Receitas

1. Localize o cartão do projeto
2. Clique no botão **"💰 + Receita"**
3. Informe:
   - **Valor**: Quantia em reais (ex: 1500.00)
   - **Data**: Data do faturamento
   - **Descrição**: Observações opcionais
4. Clique em **"✅ Salvar"**

### 🔄 Movendo Projetos Entre Etapas

**Método 1: Botões de Navegação**
- **⬅️**: Move para etapa anterior
- **➡️**: Move para próxima etapa

**Método 2: Edição**
- Clique em **"✏️ Editar"** no cartão
- Modifique as informações desejadas
- Salve as alterações

### 🎯 Abrindo Projetos no VS Code

1. Configure a **Pasta Local** do projeto
2. Clique em **"🎯 Abrir VS Code"**
3. O projeto será aberto automaticamente

## ⚙️ Configurações do Banco de Dados

O sistema cria automaticamente as seguintes tabelas:

### `etapas`
- Armazena as 4 etapas do Kanban
- Cada etapa tem ID, nome e ordem

### `projetos`
- Informações completas dos projetos
- Referência à etapa atual
- Timestamps de criação e atualização

### `faturamentos`
- Histórico de receitas por projeto
- Valor, data e descrição de cada faturamento

### `view_receita_projetos`
- VIEW que calcula receita total por projeto
- Atualizada automaticamente

## 🎨 Paleta de Cores

O sistema usa uma paleta moderna baseada em Material Design:

- **🔵 Primária**: `#2563EB` (Azul moderno)
- **✅ Sucesso**: `#10B981` (Verde)
- **⚠️ Aviso**: `#F59E0B` (Laranja)
- **❌ Erro**: `#EF4444` (Vermelho)
- **ℹ️ Info**: `#06B6D4` (Ciano)

## 🛠️ Solução de Problemas

### ❌ Erro de Conexão MySQL

1. Verifique se o MySQL está rodando
2. Confirme usuário e senha no arquivo `.env` ou `main.py`
3. Teste a conexão: `mysql -u root -p`

### 🚫 VS Code não Abre

1. Instale o VS Code: https://code.visualstudio.com/
2. Adicione VS Code ao PATH do sistema
3. Teste no terminal: `code --version`

### 🐛 Interface não Aparece

1. Verifique se CustomTkinter está instalado:
   ```bash
   pip install customtkinter
   ```
2. Teste a instalação:
   ```python
   import customtkinter
   print("CustomTkinter instalado com sucesso!")
   ```

### 🔧 Logs de Debug

Para ativar logs detalhados, edite `main.py`:

```python
# Adicione no início do arquivo
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Funcionalidades Futuras

- [ ] **Drag & Drop** entre colunas
- [ ] **Filtros e busca** de projetos
- [ ] **Relatórios de faturamento** em PDF
- [ ] **Backup automático** do banco
- [ ] **Temas personalizáveis** (claro/escuro)
- [ ] **Gráficos de produtividade**
- [ ] **Integração com Git** para status dos repos
- [ ] **Notificações** para prazos

## 📊 Estatísticas

- ✅ **100% funcional** - Todas as features implementadas
- 🎨 **Design moderno** - Interface CustomTkinter otimizada
- 🚀 **Performance** - Atualizações em tempo real via Observer
- 🔒 **Confiável** - Tratamento robusto de erros
- 📱 **Responsivo** - Layout adapta-se a diferentes resoluções

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. **Commit** suas mudanças:
   ```bash
   git commit -m 'Adiciona nova funcionalidade'
   ```
4. **Push** para a branch:
   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. Abra um **Pull Request**

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- **CustomTkinter** pela interface moderna e elegante
- **MySQL** pela robustez do banco de dados
- **Python** pela simplicidade e poder da linguagem

## 📧 Suporte

Para reportar bugs ou solicitar features:
- 🐛 Abra uma **issue** no GitHub
- 💬 Entre em contato via email
- 📝 Consulte a documentação

---

<p align="center">
  <strong>Desenvolvido com ❤️ usando Python, CustomTkinter e MySQL</strong>
</p>

<p align="center">
  ⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
</p>