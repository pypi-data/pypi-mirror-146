# Technobabble

`technobabble` is a fake Python library to let me test setup.py shenanigans.

## Usage

```python
from technobabble import Babbler

Babbler.spout()  # normal meme
Babbler.spout_softly()  # whispered lowercase meme
```

## Installation

```shell
# The one with the bug
pip install technobabble==1.0.0

# The non-leaky one
pip install technobabble==1.0.1
```

## PyPI

```shell
python setup.py sdist && twine upload dist/* 
```
