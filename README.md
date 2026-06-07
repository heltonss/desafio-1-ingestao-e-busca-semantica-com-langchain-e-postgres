# Desafio MBA Engenharia de Software com IA - Full Cycle

Aplicação de RAG (Retrieval Augmented Generation) que ingere documentos PDF e permite fazer buscas semânticas com respostas geradas por IA.

## Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Chave de API da OpenAI

## Como Executar

### 1. Clonar o repositório e navegar para a pasta

```bash
cd mba-ia-desafio-ingestao-busca
```

### 2. Instalar a versão correta do Python (isolado com pyenv)

Para não atrapalhar o ambiente da sua máquina, use **pyenv** para instalar a versão específica:

**Se não tiver pyenv instalado:**
- macOS: `brew install pyenv`
- Linux: Veja https://github.com/pyenv/pyenv#installation

**Instalar Python 3.11:**

```bash
pyenv install 3.11.15
pyenv local 3.11.15
```

### 3. Criar e ativar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
PDF_PATH=/caminho/para/seu/arquivo.pdf
OPENAI_MODEL=gpt-4o-mini
PGVECTOR_URL=postgresql://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=documents
OPENAI_API_KEY=sua_chave_api_openai
```

### 6. Iniciar o PostgreSQL com Docker

```bash
docker-compose up -d
```

Aguarde alguns segundos para que o banco de dados esteja pronto.

### 7. Ingerir os documentos PDF

```bash
python src/ingest.py
```

Isso carregará o PDF, dividirá em chunks e armazenará os embeddings no PostgreSQL.

### 8. Fazer buscas no chat

```bash
python src/chat.py "Sua pergunta aqui"
```
Se nenhuma pergunta for fornecida, usará a pergunta padrão:

```bash
python src/chat.py
```

## Exemplos de Prompts

Aqui estão alguns exemplos de prompts que você pode usar:

1. **Busca por Empresa:**
```bash
python src/chat.py "Qual é a empresa com o maior faturamento?"
```

2. **Análise Comparativa:**
```bash
python sr/chat.py "Quantas empresas tem dourado no nome?"   ```

3. **Tendências e Padrões:**
```bash
python src/chat.py "Quais são as 3 empresas com o maior faturamento"
```

## Parar a aplicação

Para desligar o PostgreSQL:

```bash
docker-compose down
```

## Estrutura do Projeto

- `src/ingest.py` - Script para ingerir PDFs e armazenar embeddings
- `src/search.py` - Módulo de busca semântica e geração de respostas
- `src/chat.py` - Interface CLI para fazer perguntas
- `docker-compose.yml` - Configuração do PostgreSQL com pgvector
- `requirements.txt` - Dependências Python