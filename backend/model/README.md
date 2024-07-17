requirments:
    - python 3.11
    - python poetry

## Installing poetry
1. python3.11 -m pip install poetry

2. poetry install

3. poetry shell

## Generate Embeddings
1. poetry run python3.11 citation_embed/embed.py

## Start ChromaDB Server
1. poetry run python3.11 start_chroma.py

# chroma issues
1. poetry add pysqlite3
or
1. poetry add pysqlite3-binary

2. uncomment these lines 
```
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
```

## Add new libs

poetry shell
poetry add chromadb

## Downloading large models
requires git lfs 
1. cd to citation_embed/saved_models/
2. git clone https://huggingface.co/dunzhang/stella_en_1.5B_v5
3. git lfs pull

# when running stell_rn_400m
1. poetry add xformers

# when running stella_en_1.5B_v5
poetry run pip install flash-attn --no-build-isolation

## Example Running Test
1. poetry run python3.11 test_retrieval.py