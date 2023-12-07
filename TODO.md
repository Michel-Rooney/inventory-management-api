
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

TODO: Campo de data de validade dos produtos
	- Criação
	- Atualização
	- Colocar na url de Alert
	- Validar na criação da compra
	- Diferenciar dos produtos que estão mais perto de vencer do que outros
  
TODO: Produto com preço de entra e saida
    - Preço de compra
    - Preço de venda

TODO: Fazer as query para ProductExpirationLog
TODO: Validar se a data não vem negativa (ontem)







1- Preciso pegar os dados da request
2- Preciso pegar o antigo_model do ValidatyProduct apartir do id e da data
3- Validar se o antigo_model realmente existe
    1. Se existir, passa a diante
    2. Se não existir, criar novo model apartir da diferença

4- Preciso validar se dadas são iguais/diferentes
    1. Se iguais, preciso analisar se a diferença é positiva ou negativa
       1. Se a diferença é positiva, adicionar ao antigo_model
       2. Se a diferença é negativa, tirar do antigo_model
          1. Se o antigo_model ficar menor que 0, então deleta-lo

    2. Se diferentes, preciso analisar se a diferença é positva ou negativa
       1. Se a diferença é positiva, criar novo model
       2. Se a diferença negativa, tirar do antigo_model já existente