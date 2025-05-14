# Sistema Kanban - Controle de Projetos

Um sistema de gerenciamento de projetos estilo Kanban com interface gráfica PyQt6, banco de dados MySQL e controle de faturamento.

## 🚀 Características

- **Interface Kanban** com drag-and-drop
- **Controle de faturamento** por projeto
- **Integração com VS Code/Visual Studio**
- **Banco de dados MySQL** para persistência
- **Arquitetura modular** seguindo padrões MVC

## 📋 Pré-requisitos

- Python 3.8+
- MySQL 5.7+ ou MariaDB 10.2+
- VS Code ou Visual Studio (opcional, para abrir projetos)

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd sistema-kanban
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

#### 4.1. Crie o banco no MySQL
```sql
-- Execute no MySQL Workbench ou linha de comando
CREATE DATABASE kanban_projects CHARACTER SET utf8mb4;
```

#### 4.2. Execute o script de criação das tabelas
```bash
mysql -u root -p kanban_projects < database_schema.sql
```

#### 4.3. Configure as credenciais
Edite o arquivo `db.py` e ajuste as configurações na classe `DatabaseConfig`:

```python
class DatabaseConfig:
    HOST = 'localhost'
    DATABASE = 'kanban_projects'
    USER = 'seu_usuario'         # Altere aqui
    PASSWORD = 'sua_senha'       # Altere aqui
    CHARSET = 'utf8mb4'
```

## 🖥️ Execução

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
sistema-kanban/
├── main.py             # Ponto de entrada da aplicação
├── gui.py              # Interface gráfica (PyQt6)
├── db.py               # Acesso ao banco de dados
├── models.py           # Modelos de domínio
├── database_schema.sql # Script de criação do banco
├── requirements.txt    # Dependências Python
├── README.md           # Este arquivo
└── logs/               # Logs da aplicação (criado automaticamente)
```

## 🎯 Como Usar

### 1. Criando um Projeto
- Clique em "➕ Novo Projeto"
- Preencha os dados (nome, descrição, pasta local, arquivo principal)
- Selecione a etapa inicial
- Clique em "💾 Salvar"

### 2. Movimentando Projetos
- Arraste os cartões entre as colunas do Kanban
- Os projetos são automaticamente atualizados no banco

### 3. Abrindo Projetos no Editor
- Clique no botão "📁 Abrir" no cartão do projeto
- O sistema tentará abrir com VS Code primeiro, depois Visual Studio

### 4. Gerenciando Faturamentos
- Clique em "✏️ Editar" no cartão do projeto
- Na seção "Faturamentos", adicione valores e datas
- O total é calculado automaticamente

## ⚙️ Configurações Avançadas

### Personalizar Etapas
Para adicionar/modificar etapas, execute no MySQL:

```sql
INSERT INTO etapas (nome, ordem) VALUES ('Nova Etapa', 5);
```

### Backup do Banco
```bash
mysqldump -u root -p kanban_projects > backup.sql
```

### Logs
Os logs são salvos em `logs/kanban.log` e incluem:
- Conexões com banco
- Operações de CRUD
- Erros e exceções

## 🔍 Solução de Problemas

### Erro de Conexão MySQL
1. Verifique se o MySQL está rodando
2. Confirme usuário e senha em `db.py`
3. Certifique-se que o banco `kanban_projects` existe

### Projetos não abrem no editor
1. Verifique se VS Code/Visual Studio estão no PATH
2. Confirme se o caminho da pasta está correto
3. Para VS Code: `code --version`
4. Para Visual Studio: `devenv /?`

### Interface não aparece
1. Verifique se PyQt6 está instalado corretamente
2. Teste com: `python -c "from PyQt6.QtWidgets import QApplication; print('OK')"`

## 🛠️ Desenvolvimento

### Executar em modo debug
```python
# Adicione no início do main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Extensões possíveis
- [ ] Autenticação de usuários
- [ ] Relatórios de faturamento
- [ ] Notificações por email
- [ ] API REST para integração
- [ ] Sincronização com Git

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📧 Contato

Desenvolvido com ❤️ em Python + PyQt6

---

⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!