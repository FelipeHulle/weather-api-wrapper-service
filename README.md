# Weather Client com Redis Cache

Este projeto tem como objetivo consumir dados de uma **API de clima** (Visual Crossing Weather API), com suporte a **cache utilizando Redis**. A solução permite que informações meteorológicas sejam armazenadas temporariamente para evitar chamadas repetitivas à API, otimizando o desempenho da aplicação.

---

## 🔧 Tecnologias Utilizadas

- Python 3.13
- [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api)
- Redis
- Docker
- `requests`
- `redis-py`
- Variáveis de ambiente com `.env`

---

## 📁 Estrutura de Arquivos

```bash
├── .venv/               # Ambiente virtual
├── .env.example         # Exemplo de .env
├── .gitignore
├── app.py               # (Ponto de entrada opcional)
├── config.py            # Configurações (API Key, Redis)
├── weather_client.py    # Cliente de API + cache Redis
├── requirements.txt     # Dependências
└── README.md            # Este arquivo
```

---

## 🚀 Instalação e Execução

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/weather-redis-client.git
cd weather-redis-client
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Suba o Redis com Docker

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

> Isso executará uma instância do Redis com RedisInsight (interface web em `http://localhost:8001`).

### 5. Configure o .env

```bash
WEATHER_KEY=your_weather_api_key
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 6. Execute o script principal

```bash
python weather_client.py
```

## 💡 Detalhes Técnicos

* Os dados são armazenados no Redis com  **expiração de 60 segundos** .
* Ao consultar uma cidade, o sistema verifica se ela já está no cache antes de chamar a API.
* A resposta é simplificada para conter apenas informações relevantes: endereço, data, temperatura máxima e mínima.
