# clorusapi

API Clorus Marketeer

## Descrição do ambiente dev

Iniciar o ambiente python na versão disponível, recomendo usar a versão `3.9.5`.

```python
python3 -m venv env
source env/bin/activate
pip install tox
```

Agora inicialize o ambiente com o tox. Esse comando irá instalar as dependências do projeto, fazer os migrations e realizar os testes se existirem.

```python
tox
```

Ative o seu ambiente

```python
source .tox/py39/bin/activate
```

Para rodar o projeto, use o seguinte comando

```python
./manage.py runserver
```

##
