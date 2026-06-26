# Revisaê-API

Revisaê é um aplicativo para gerenciar conteúdos estudados que precisam ser revisados. Esse repositório compreende a API a ser utilizada pelo aplicativo. A ideia inicial foi tentar seguir uma estrutura baseada em Clean Architecture.

## Arquitetura

A arquitetura, resumida, de pastas da aplicação segue o seguinte modelo:

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
|   |   ├── consumers/                  # consumers para lidar com os eventos de domínio
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
