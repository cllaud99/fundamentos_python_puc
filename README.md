# Fundamentos de Python - PUC Minas

Projeto acadêmico para a disciplina de Fundamentos de Python da Pós-graduação em Engenharia de Dados da PUC Minas, utilizando Python 3.12 e `uv` para gerenciamento de dependências.

## 🚀 Recursos Principais

- Integração com 3 APIs externas:
  - AirVisual (qualidade do ar)
  - Countries API (dados de países)
  - Weather API (previsão do tempo)
- Sistema inteligente de cache em CSV
- Integração com PostgreSQL via Docker
- 10 exercícios práticos de Python
- Pipeline de formatação automática de código
- Ambiente configurado com Docker e pgAdmin

## 📁 Estrutura do Projeto

```
fundamentos_python_puc/
├── data/                      # Dados salvos do projeto
│   ├── cache/                 # Cache das chamadas da API
│   ├── pics/                  # Gráficos gerados nos exercícios
│   └── reports/               # Arquivos XLSX gerados
├── pagila/                    # Repositório clonado com base de dados
├── src/                       # Código-fonte principal
│   ├── cache/                 # Sistema de cache inteligente
│   ├── db/                    # Módulo de acesso ao banco de dados
│   │   ├── sql/               # Consultas SQL dos exercícios
│   │   └── db_handler.py      # Conexão e manipulação do banco
│   ├── services/              # Integrações com APIs externas
│   │   ├── airvisual.py
│   │   ├── countries.py
│   │   └── weather.py
│   ├── exercicios_resolucoes/ # Lista de exercícios resolvidos
│   └── main.py                # Arquivo principal de execução
├── .env.example               # Exemplo de variáveis de ambiente
├── pyproject.toml             # Configuração de dependências
├── requirements.txt           # Dependências para instalação via pip
└── README.md                  # Este arquivo
```

## 📋 Pré-requisitos

- Python 3.12
- Docker e Docker Compose
- [`uv`](https://github.com/astral-sh/uv) (gerenciador de pacotes ultrarrápido — opcional, mas recomendado)

## 🛠️ Instalação

1. **Clonar o repositório:**

```
git clone https://github.com/cllaud99/fundamentos_python_puc.git
cd fundamentos_python_puc
```

2. **Escolha uma das opções abaixo para instalar as dependências:**

### 👉 Opção 1: Usando UV (recomendado)

> O `uv` já cria e gerencia um ambiente virtual automaticamente.

```
uv pip install -r requirements.txt
```

### 👉 Opção 2: Usando pip e ambiente virtual manual

3. Criar e ativar o ambiente virtual:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

4. Instalar as dependências:

```
pip install -r requirements.txt
```

5. Copiar as variáveis de ambiente:

```
cp .env.example .env
```

## 🐳 Executar Banco de Dados

Dentro da pasta `pagila`, execute o seguinte comando para iniciar o banco PostgreSQL com Docker:

```
cd pagila
docker-compose up -d
```