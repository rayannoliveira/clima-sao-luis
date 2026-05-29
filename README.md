# Projeto PySpark - Clima de São Luís

## Visão Geral

Este projeto consome dados da API Open-Meteo e processa as informações utilizando PySpark, seguindo a arquitetura Medalhão (Medallion Architecture) composta pelas camadas Bronze, Silver e Gold.

O objetivo é demonstrar conceitos de Engenharia de Dados como ingestão de APIs, processamento distribuído com Spark, transformação de dados e organização em camadas analíticas.

---

## Objetivo

Coletar dados climáticos de São Luís - MA através da API Open-Meteo, armazenar os dados brutos e gerar informações tratadas para análise de temperatura e condições climáticas.

---

## Tecnologias Utilizadas

* Python 3.9+
* PySpark
* Apache Spark
* Open-Meteo API
* Docker (opcional)
* Git

---

## Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

### 1. Git

Instalação:

https://git-scm.com/downloads

Verificar instalação:

```bash
git --version
```

### 2. Python 3.9+

Verificar versão:

```bash
python --version
```

ou

```bash
py --version
```

### 3. Pip

Verificar:

```bash
pip --version
```

### 4. Java

O Spark depende do Java.

Verificar instalação:

```bash
java -version
```

Recomendado:

* Java 11
* Java 17

### 5. Apache Spark / PySpark

Instalar PySpark:

```bash
pip install pyspark
```

Verificar:

```bash
pip show pyspark
```

### 6. Docker (Opcional)

O Docker pode ser utilizado para executar aplicações em containers.

Verificar instalação:

```bash
docker --version
```

Verificar se o daemon está rodando:

```bash
docker ps
```

Se o comando retornar uma tabela (mesmo vazia), o Docker está funcionando corretamente.

---

## Fonte dos Dados

API utilizada:

https://api.open-meteo.com

Endpoint utilizado:

```text
https://api.open-meteo.com/v1/forecast?latitude=-2.5297&longitude=-44.3028&hourly=temperature_2m,weather_code
```

---

## Dados Coletados

A API retorna:

| Campo          | Descrição                    |
| -------------- | ---------------------------- |
| time           | Data e hora da medição       |
| temperature_2m | Temperatura em °C            |
| weather_code   | Código da condição climática |

---

## Arquitetura Medalhão

### Bronze

Camada responsável por armazenar os dados brutos exatamente como recebidos da API.

Exemplo:

```text
data/bronze/weather_raw/open_meteo_raw.json
```

Características:

* Sem transformações
* Fonte histórica
* Permite reprocessamento

---

### Silver

Camada de limpeza e enriquecimento.

Transformações realizadas:

* Conversão de timestamp
* Tradução dos códigos climáticos
* Padronização dos tipos de dados

Exemplo:

| timestamp        | temperature | weather_description |
| ---------------- | ----------- | ------------------- |
| 2026-05-29 10:00 | 30.1        | Céu limpo           |

---

### Gold

Camada analítica.

Agregações realizadas:

* Temperatura média diária
* Temperatura máxima diária
* Temperatura mínima diária

Exemplo:

| data       | temp_media | temp_max | temp_min |
| ---------- | ---------- | -------- | -------- |
| 2026-05-29 | 30.2       | 33.1     | 27.8     |

---

## Estrutura do Projeto

```text
projeto-clima/

├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

---

## Fluxo do Pipeline

1. Consumir dados da API Open-Meteo.
2. Armazenar resposta bruta na camada Bronze.
3. Ler dados com PySpark.
4. Traduzir códigos meteorológicos.
5. Criar camada Silver tratada.
6. Gerar métricas agregadas.
7. Salvar resultados na camada Gold.

---

## Executando o Projeto

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar:

```bash
python main.py
```

ou

```bash
spark-submit main.py
```

---

## Exemplo de Saída

### Silver

```text
+-------------------+-----------+---------------------+
| timestamp         | temperature | weather_description |
+-------------------+-----------+---------------------+
| 2026-05-29 10:00  | 30.1      | Céu limpo           |
+-------------------+-----------+---------------------+
```

### Gold

```text
+----------+-----------+----------+----------+
| data     | temp_media| temp_max | temp_min |
+----------+-----------+----------+----------+
|2026-05-29|30.2       |33.1      |27.8      |
+----------+-----------+----------+----------+
```

---

## Conceitos Demonstrados

* Consumo de APIs REST
* Engenharia de Dados
* Apache Spark
* PySpark DataFrames
* UDFs
* Arquitetura Medalhão
* ETL/ELT
* Processamento distribuído
* Transformação de dados

---

## Melhorias Futuras

* Escrita em formato Parquet
* Particionamento por data
* Dockerização da aplicação
* Integração com Airflow
* Armazenamento em Data Lake
* Monitoramento e logging
* Testes automatizados

---

## Autor

Rayanne Oliveira

Data Engineer
