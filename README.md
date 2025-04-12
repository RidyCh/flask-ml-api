# Flask API for NilaiKu

App Flask untuk integrasi model Nilaiku


## Pustaka
 - [flask]
 - [pandas]
 - [numpy]
 - [scikit-learn]
 - [xgboost]
 - [gunicorn]
 - [python-dotenv]
 - [scikit-optimize]

## API Features

- get - / (check api)
- post - predict

## API Reference

#### Get all items

```http
  GET /
```

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. c43649ac42bc8e0259106ffd7cb9571cda6a03a1010d2c2c6415bab08dbf98e3 |

#### Get item

```http
  POST /predict
```

| Header | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. c43649ac42bc8e0259106ffd7cb9571cda6a03a1010d2c2c6415bab08dbf98e3 |


## Installation

Install my-project with npm

```bash
  git clone https://github.com/RidyCh/flask-ml-api
  cd my-project
```
Install paket
**Pastikan memiliki python terlebih dahulu dengan mengecek di terminal python --version**

```bash
  pip install <nama_paket>
```

## Running 

Mulai app

```bash
  python app.py
```

Tambahkan http get dipostman atau lainnya 
- http://127.0.0.1:5001/ (untuk api check)

- http://127.0.0.1:5001/predict (untuk post prediksi dengan menambahkan kolom yang ada)

