# 🔎 API de Busca Semântica com Flask + PostgreSQL

Este projeto implementa um **motor de busca semântica** baseado em:

* Bag of Words (BOW)
* Similaridade de cosseno
* Integração com banco de dados PostgreSQL

O sistema recebe uma pergunta em linguagem natural e retorna resultados a partir de consultas SQL.

---

# 🚀 Tecnologias utilizadas

* Python 3.12
* Flask
* SQLAlchemy
* PostgreSQL
* Scikit-learn (BOW + similaridade)
* Docker

---


# ⚙️ Como rodar o projeto

## 1. Clonar o repositório

```
git clone https://github.com/Code-Nine-FTC/representation-nlp.git
```

---

## 2. Subir o banco com Docker

```
docker-compose up -d
```

Isso irá:

* Criar o banco PostgreSQL
* Criar a tabela `people_images`
* Inserir dados iniciais

---

## 3. Criar ambiente virtual

```
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Windows
.venv\Scripts\activate
```

---

## 4. Instalar dependências

```
pip install -r requirements.txt
```


## 5. Configurar conexão com banco

No arquivo `database.py`:

```python
engine = create_engine("postgresql://postgres:postgres@localhost:5432/peopledb")
```

---

## 6. Rodar a API

```
python api/app.py
```

A API estará disponível em:

```
http://localhost:5000
```

---

# 💬 Front-end (modo noturno)

Depois de subir o banco e rodar a API, acesse no navegador:

```
http://localhost:5000/
```

Você verá uma interface de chat em **modo noturno** (estilo ChatGPT) que chama o endpoint `POST /search`.

---

# 🔍 Como testar

## Endpoint

```
POST /search
```

## Exemplo com curl

```
curl -X POST http://localhost:5000/search \
-H "Content-Type: application/json" \
-d '{"query": "quantas pessoas existem?"}'
```

---

## 🧪 Exemplos de consultas

* "quantas pessoas existem?"
* "mostrar pessoas com cabelo loiro"
* "pessoas negras"

---

# 📤 Exemplo de resposta

```json
{
  "query_interpretada": 0,
  "sql": "SELECT COUNT(*) FROM people_images",
  "resultado": 5
}
```

---

# 🧠 Como funciona

1. Usuário envia uma query em linguagem natural
2. Texto é transformado em Bag of Words
3. Comparação com queries conhecidas (similaridade de cosseno)
4. Seleção da query mais próxima
5. Execução no banco de dados
6. Retorno dos resultados
