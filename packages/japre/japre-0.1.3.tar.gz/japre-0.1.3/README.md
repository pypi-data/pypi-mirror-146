# japanese_pretokenizers (japre)

Custom pretokenizers for Japanese language models

## installation

```
pip install japre
```

## Usage

### IpadicPreTokenizer

```python
from japre.ipadic import IpadicPreTokenizer

from transformers import PreTrainedTokenizerFast
from tokenizers import Tokenizer

tokenizer_object = Tokenizer.from_file("your-awesome-tokenizer.json")
tokenizer_object.pre_tokenizer = IpadicPreTokenizer.make()
tokenizer = PreTrainedTokenizerFast(
    tokenizer_object=tokenizer_object,
    unk_token='[UNK]',
    mask_token='[MASK]',
    cls_token='[CLS]',
    pad_token='[PAD]',
    sep_token='[SEP]'
)
```

### ManbyoDictPreTokenizer

```
export MANBYO_DICT_PATH=/path/to/MANBYO_201907_Dic-utf8.dic
```

```python
from japre.manbyo import ManbyoDictPreTokenizer

from transformers import PreTrainedTokenizerFast
from tokenizers import Tokenizer

tokenizer_object = Tokenizer.from_file("your-awesome-tokenizer.json")
tokenizer_object.pre_tokenizer = ManbyoDictPreTokenizer.make()
tokenizer = PreTrainedTokenizerFast(
    tokenizer_object=tokenizer_object,
    unk_token='[UNK]',
    mask_token='[MASK]',
    cls_token='[CLS]',
    pad_token='[PAD]',
    sep_token='[SEP]'
)
```