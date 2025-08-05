# 📋 Sistema de Gestão de Formulários - API REST

## 🎯 Visão Geral

Este é um sistema completo de gestão de formulários desenvolvido com **FastAPI** e **SQLModel**. O sistema permite criar formulários dinâmicos com diferentes tipos de questões (abertas e múltipla escolha), gerenciar usuários e coletar respostas de forma estruturada.

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas bem definida:

```
📁 desafio_tecnico/
├── 📁 controllers/          # Controladores da API (rotas)
├── 📁 models/              # Modelos de dados (SQLModel)
├── 📁 repositories/        # Camada de acesso a dados
├── 📁 schemas/             # Schemas de validação (Pydantic)
├── 📁 uploads/             # Arquivos de upload
├── 📄 config.py            # Configuração do banco de dados
├── 📄 dependencies.py      # Injeção de dependências
├── 📄 main.py              # Ponto de entrada da aplicação
└── 📄 pyproject.toml       # Configuração do projeto
```

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[SQLModel](https://sqlmodel.tiangolo.com/)** - ORM baseado em SQLAlchemy e Pydantic
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados relacional
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI de alta performance
- **[Poetry](https://python-poetry.org/)** - Gerenciamento de dependências

## 📊 Modelo de Dados

### Entidades Principais

#### 👤 Usuários
- **id**: Identificador único
- **nome**: Nome do usuário
- **email**: Email único
- **senha**: Senha criptografada
- **ativo**: Status do usuário
- **data_criacao/modificacao/desativacao**: Timestamps

#### 📝 Formulários
- **id**: Identificador único
- **titulo**: Título do formulário
- **descricao**: Descrição detalhada
- **ativo**: Status do formulário
- **usuario_id**: Criador do formulário
- **data_criacao/modificacao/desativacao**: Timestamps

#### ❓ Questões
- **id**: Identificador único
- **enunciado**: Texto da questão
- **tipo**: Tipo da questão (aberta, multipla_escolha)
- **ativo**: Status da questão
- **formulario_id**: Formulário ao qual pertence

#### 🔤 Alternativas (para questões de múltipla escolha)
- **id**: Identificador único
- **texto**: Texto da alternativa
- **correta**: Se é a resposta correta
- **ativo**: Status da alternativa
- **questao_id**: Questão à qual pertence

#### 💬 Respostas
- **id**: Identificador único
- **valor**: Resposta em texto (para questões abertas)
- **alternativa_id**: Referência à alternativa escolhida (múltipla escolha)
- **questao_id**: Questão respondida
- **usuario_id**: Usuário que respondeu
- **data_criacao/modificacao**: Timestamps

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL
- Poetry (opcional, mas recomendado)

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd desafio_tecnico
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=nome_do_banco
POSTGRES_HOST=localhost
```

### 3. Instale as dependências

#### Com Poetry:
```bash
poetry install
poetry shell
```

#### Com pip:
```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python main.py
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

### Acesso à Documentação Interativa

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Principais Endpoints

#### 👤 Usuários (`/api/v1/usuarios`)
- `GET /usuarios` - Listar usuários
- `GET /usuarios/{id}` - Buscar usuário por ID
- `POST /usuarios` - Criar usuário

#### 📝 Formulários (`/api/v1/formularios`)
- `GET /formularios` - Listar formulários
- `GET /formularios/{id}` - Buscar formulário por ID
- `POST /formularios` - Criar formulário
- `PUT /formularios/{id}` - Atualizar formulário
- `DELETE /formularios/{id}` - Deletar formulário

#### ❓ Questões (`/api/v1/questoes`)
- `GET /questoes` - Listar questões
- `GET /questoes/{id}` - Buscar questão por ID
- `POST /questoes` - Criar questão
- `PUT /questoes/{id}` - Atualizar questão
- `DELETE /questoes/{id}` - Deletar questão

#### 🔤 Alternativas (`/api/v1/alternativas`)
- `GET /alternativas` - Listar alternativas
- `GET /alternativas/{id}` - Buscar alternativa por ID
- `GET /questoes/{questao_id}/alternativas` - Alternativas por questão
- `POST /alternativas` - Criar alternativa
- `PUT /alternativas/{id}` - Atualizar alternativa
- `DELETE /alternativas/{id}` - Deletar alternativa

#### 💬 Respostas (`/api/v1/respostas`)
- `GET /respostas` - Listar respostas
- `GET /respostas/{id}` - Buscar resposta por ID
- `GET /usuarios/{usuario_id}/respostas` - Respostas por usuário
- `GET /questoes/{questao_id}/respostas` - Respostas por questão
- `POST /respostas` - Criar resposta
- `POST /questoes/{questao_id}/responder-texto` - Responder questão aberta
- `POST /questoes/{questao_id}/alternativas/{alternativa_id}/responder` - Responder múltipla escolha
- `PUT /respostas/{id}` - Atualizar resposta
- `DELETE /respostas/{id}` - Deletar resposta

## 💡 Exemplos de Uso

### Criando um Usuário

```bash
curl -X POST "http://localhost:8000/api/v1/usuarios" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "João Silva",
       "email": "joao@email.com",
       "senha": "senha123"
     }'
```

### Criando um Formulário

```bash
curl -X POST "http://localhost:8000/api/v1/formularios" \
     -H "Content-Type: application/json" \
     -d '{
       "titulo": "Pesquisa de Satisfação",
       "descricao": "Avaliação do nosso serviço",
       "usuario_id": 1
     }'
```

### Criando uma Questão de Múltipla Escolha

```bash
curl -X POST "http://localhost:8000/api/v1/questoes" \
     -H "Content-Type: application/json" \
     -d '{
       "enunciado": "Como você avalia nosso atendimento?",
       "tipo": "multipla_escolha",
       "formulario_id": 1
     }'
```

### Criando Alternativas

```bash
curl -X POST "http://localhost:8000/api/v1/alternativas" \
     -H "Content-Type: application/json" \
     -d '{
       "texto": "Excelente",
       "correta": false,
       "questao_id": 1
     }'
```

### Respondendo uma Questão de Múltipla Escolha

```bash
curl -X POST "http://localhost:8000/api/v1/questoes/1/alternativas/1/responder?usuario_id=1"
```

### Respondendo uma Questão Aberta

```bash
curl -X POST "http://localhost:8000/api/v1/questoes/2/responder-texto?usuario_id=1&valor=Muito%20satisfeito"
```

## 🔧 Funcionalidades Avançadas

### Filtros e Paginação
- Todos os endpoints de listagem suportam paginação (`skip` e `limit`)
- Filtros por status ativo/inativo
- Filtros por relacionamentos (ex: questões por formulário)

### Validações de Negócio
- Um usuário não pode responder a mesma questão duas vezes
- Questões de múltipla escolha só aceitam alternativas válidas
- Questões abertas só aceitam texto
- Validação de tipos de resposta (não é possível enviar ambos)

### Soft Delete
- Usuários, formulários e questões podem ser desativados ao invés de deletados
- Preserva integridade referencial
- Permite recuperação de dados

### Exemplo de Fluxo Completo

1. Criar um usuário administrador
2. Criar um formulário
3. Adicionar questões (abertas e múltipla escolha)
4. Adicionar alternativas para questões de múltipla escolha
5. Criar usuários respondentes
6. Coletar respostas
7. Analisar resultados

## 👨‍💻 Autor

**Luis Bezerra Barradas**
- Email: luisbezerrabarradas@gmail.com