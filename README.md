# Projeto PySpark - Clima de São Luís

Este projeto consome dados da API gratuita Open-Meteo e processa as informações usando PySpark, seguindo uma arquitetura em camadas no modelo Medalhão: Bronze, Silver e Gold.

## Objetivo

O objetivo do projeto é coletar dados climáticos de São Luís - MA, armazenar o dado bruto e transformar as informações para análise diária de temperatura.

## Fonte dos dados

API utilizada:

https://api.open-meteo.com

A API retorna dados como:

- horário da medição
- temperatura
- código climático

## Arquitetura Medalhão

### Bronze

Camada onde o JSON bruto da API é salvo sem tratamento.

Exemplo:

```text
data/bronze/weather_raw/open_meteo_raw.json
