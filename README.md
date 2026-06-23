# Revisaê-API

Arquitetura de pastas da aqplicação:

```
revisae-api
├── src/
|   ├── domain/
|   |   ├── entities/                   # entidades
|   |   ├── events                      # eventos para processamento asíncrono
|   |   ├── exceptions                  # exceptions para tratamento de erro
|   |   ├── repositories                # ports de repositório para entidades do domínio
|   |   └── value_objects               # objetos de valores (Email, HashedPassword, etc.)
|   |
|   ├── application/
|   |   ├── interfaces/                 # interfaces comuns e de serviço
|   |   ├── schemas/                    # schemas usados nos use-cases
|   |   └── use_cases/                  # use-cases com regras de negócio
|   |
|   ├── infraestructure/
|   |   ├── config/                     # configurações da aplicação com dynaconf
|   |   ├── database/                   # models do banco de dados
|   |   ├── mappers/                    # mapeamento entre entidades e models
|   |   └── providers/                  # configura providers de dependencias
|   |
|   ├── presentation/
|   |   ├── http_schemas/               # schemas utilizados nas requisições http
|   |   ├── routers/                    # mapeamento de rotas e use-cases
|   |   ├── ...
|   |   ├── dependencies.py             # dependencies do fastapi
|   |   └── exception_handlers.py       # exception handlers do fastapi
|   |
|   └── adapters/
|       ├── repositories/               # repositórios do banco de dados e entidades
|       └── services/                   # service providers para ports de application/interfaces
|
```
