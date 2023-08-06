# simple-storage-service

This package is intended to assist in the handling of files on storages from different providers.

Currently, this project supports 3 providers: AWS, Azure and GCP.

## Getting started

### Install

```sh
pip install storage-service
```

### Initialize a storage provider

```python
from simple_storage_service import SimpleStorage

simple_storage = SimpleStorage.initialize('GCP', {'bucket_name': 'some-bucket'})
simple_storage.get_object('some-key')
simple_storage.upload_object('some-key', 'path/to/file.txt')
```

## Colaborating

### Run tests

python -m unittest discover tests

## Deploy

### Change version on setup.py

### Remove previous version

```sh
rm -rf dist
```

### Build project

```sh
python -m build
```

### Upload project

```sh
python -m twine upload dist/*
```
