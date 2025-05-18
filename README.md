# Modelo preditivo LSTM

## Descrição  
Com base em um dado histórico da bolsa de valores, o modelo deve predizer qual foi o valor de fechamento.


## Endpoints Principais  

### GET /health
```bash
Descrição: Captura se a API está no ar, simplesmente.

### POST /predict
```bash
Descrição: Com base em um determinado dataset contendo dados históricos da bolsa, a API retorna a previsão de fechamento.

Requisição:

{
    {"test_data": [[0.07438016537496309], [0.07394519407214892], [0.08568942961866582], [0.08916920004117931], [0.08742931482992258], [0.08960418171452739], [0.09351893381038895], [0.09395389474266927], [0.09090908525243607]...
}

Resposta:


{
    "prediction": -0.8172371983528137
}

```

### GET /metrics
```bash
Descrição: Captura algumas métricas sobre as requisições feitas à API

Resposta:
{
    "/": 1,
    "/health": 4,
    "/metrics": 6,
    "/predict": 1
}
```


# Informações de contato

## Autor  
Desenvolvido por: 

André Vicente Torres Martins
E-mail: andrasno@gmail.com

Nathan Rafael Pedroso Lobato.
E-mail: nathan.lobato@outlook.com.br

