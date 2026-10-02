# API de Pacientes — FastAPI

API REST simples para cadastro e gerenciamento de pacientes, desenvolvida com FastAPI, SQLModel e SQLite.

## Funcionalidades

- CRUD completo de pacientes (criar, listar, buscar, atualizar, excluir)
- Validação de dados com Pydantic/SQLModel
- Condições médicas restritas a um conjunto fixo de valores (Enum)
- Paginação e filtro por condição na listagem
- Tratamento de erros padronizado
- Persistência em banco de dados SQLite
- Testes automatizados com pytest

## Tecnologias

- Python 3.13
- FastAPI
- SQLModel
- SQLite
- pytest

## Como rodar

1. Instale as dependências:
```bash
pip install fastapi uvicorn sqlmodel pytest httpx
```

2. Inicie o servidor:
```bash
uvicorn main:app --reload
```

3. Acesse a documentação interativa: http://127.0.0.1:8000/docs

4. 
## Rodando os testes

```bash
pytest
```

## Endpoints

| Método | Rota             | Descrição                        |
|--------|------------------|-----------------------------------|
| POST   | /patients        | Cria um novo paciente             |
| GET    | /patients        | Lista pacientes (paginação/filtro)|
| GET    | /patients/{id}   | Busca um paciente por ID          |
| PUT    | /patients/{id}   | Atualiza um paciente              |
| DELETE | /patients/{id}   | Remove um paciente                |