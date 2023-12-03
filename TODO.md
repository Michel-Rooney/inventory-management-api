
USER {
    GET:
        - ME
}

PRODUCTS {
    GET:
      - LIST
      - ID
      - SEARCH
  
    POST:
        - CREATE

    PATCH:
        - UPDATE
  
    DELETE:
        - DELETE
}

LOG_BUY {
    GET:
        - MÉDIA
}

LOG_PRODUCTS {
    PK
}


[X] TODO: Validar se tem produto no estoque para fazer a compra
[X] TODO: Criar url de produtos que estão perto de acabar
[X] TODO: Validar se os produtos que vem tem quantidade positiva
