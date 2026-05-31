# Projeto ETL Clima São Luís

Projeto de Engenharia de Dados desenvolvido com Python, PySpark, PostgreSQL, Docker e Apache Airflow para consumo de dados meteorológicos da API Open-Meteo, seguindo a arquitetura Medalhão (Bronze, Silver e Gold).

---

# Objetivo

O objetivo deste projeto é coletar dados climáticos da cidade de São Luís - MA através da API Open-Meteo, armazenar os dados brutos, realizar transformações e gerar informações analíticas para consulta e monitoramento.

---

# Tecnologias Utilizadas

- Python 3.11
- PySpark
- PostgreSQL
- Apache Airflow
- Docker
- Docker Compose
- Open-Meteo API
- Git

---

# Fonte dos Dados

API utilizada:

https://open-meteo.com/

Endpoint:

```text
https://api.open-meteo.com/v1/forecast
```

Dados coletados:

- Data e hora da medição
- Temperatura
- Código meteorológico
- Descrição meteorológica

---

# Arquitetura Medalhão

```text
Open-Meteo API
        │
        ▼
    Bronze
(JSON bruto)
        │
        ▼
    Silver
(Dados tratados)
        │
        ▼
     Gold
(Métricas diárias)
        │
        ▼
 PostgreSQL
        │
        ▼
 Apache Airflow
(Orquestração)
```

---

# Camada Bronze

A camada Bronze é responsável por armazenar os dados brutos retornados pela API sem qualquer transformação.

Exemplo:

```json
{
  "time": "2026-06-01T00:00",
  "temperature_2m": 26.5,
  "weather_code": 3
}
```

Local de armazenamento:

```text
data/bronze/weather_raw/
```

---

# Camada Silver

A camada Silver realiza o tratamento e enriquecimento dos dados.

Transformações realizadas:

- Conversão dos timestamps
- Tradução dos códigos meteorológicos
- Padronização dos dados
- Inclusão da data de extração
- Preparação para análise

Estrutura:

| timestamp | temperature | weather_code | weather_description | extraction_date |
|------------|------------|------------|------------|------------|
| 2026-06-01 10:00 | 30.1 | 0 | Céu limpo | 2026-05-31 |

Exemplo:

```python
.withColumn(
    "extraction_date",
    current_date()
)
```

---

# Camada Gold

A camada Gold contém métricas prontas para consumo.

Agregações realizadas:

- Temperatura média diária
- Temperatura máxima diária
- Temperatura mínima diária
- Histórico das previsões por data de extração

Estrutura:

| forecast_date | extraction_date | avg_temperature | max_temperature | min_temperature |
|---------------|----------------|-----------------|-----------------|-----------------|
| 2026-06-05 | 2026-05-30 | 26.1 | 29.5 | 24.2 |

Exemplo de cálculo:

```python
.groupBy(
    "forecast_date",
    "extraction_date"
)
.agg(
    avg("temperature").alias("avg_temperature"),
    max("temperature").alias("max_temperature"),
    min("temperature").alias("min_temperature")
)
```

---

# Estrutura do Projeto

```text
clima-sao-luis/

├── dags/
│   └── clima_dag.py
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── data/
│   └── bronze/
│
├── docker-compose.yml
├── Dockerfile.airflow
├── requirements.txt
└── README.md
```

---

# PostgreSQL

Os dados processados são armazenados em PostgreSQL.

Banco:

```text
clima_db
```

Tabelas:

```text
silver_weather
gold_weather_daily
```

Exemplos de consultas:

```sql
SELECT * FROM silver_weather LIMIT 10;

SELECT * FROM gold_weather_daily LIMIT 10;
```

Contagem de registros:

```sql
SELECT COUNT(*) FROM silver_weather;

SELECT COUNT(*) FROM gold_weather_daily;
```

---

# Docker

## Construir e iniciar containers

```bash
docker compose up --build -d
```

## Parar containers

```bash
docker compose down
```

## Visualizar containers

```bash
docker ps
```

## Visualizar logs

```bash
docker logs airflow-clima

docker logs postgres-climas
```

---

# Apache Airflow

O Apache Airflow é responsável pela orquestração do pipeline.

Fluxo executado:

1. Extração dos dados da API
2. Criação da camada Bronze
3. Transformação para Silver
4. Criação da camada Gold
5. Escrita no PostgreSQL

Arquivo da DAG:

```text
dags/clima_dag.py
```

Acesso à interface:

```text
http://localhost:8080
```

Usuário:

```text
admin
```

Senha:

```text
admin123
```

---

# Agendamento da DAG

Exemplo para execução diária às 15h:

```python
schedule="0 15 * * *"
```

Formato Cron:

```text
┌──────── minuto
│ ┌────── hora
│ │ ┌──── dia do mês
│ │ │ ┌── mês
│ │ │ │ ┌ dia da semana
│ │ │ │ │
0 15 * * *
```

---

# Como Executar Localmente

## Criar ambiente virtual

```bash
python -m venv venv
```

## Ativar ambiente

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Executar pipeline

```bash
python src/pipeline.py
```

---

# Possíveis Evoluções

- Armazenamento em Parquet
- Particionamento por data
- Testes unitários
- Integração com MinIO
- Integração com Data Lake
- Monitoramento com Prometheus
- Dashboards com Grafana
- Deploy em GCP
- Deploy em AWS

---

# Autor

Rayanne Oliveira

Data Engineer | Python | PySpark | PostgreSQL | Airflow | Docker