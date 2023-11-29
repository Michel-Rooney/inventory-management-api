
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
