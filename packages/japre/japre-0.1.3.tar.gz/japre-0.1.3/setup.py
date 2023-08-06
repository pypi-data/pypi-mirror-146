# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['japre']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.1,<5.0.0',
 'fugashi>=1.1.2,<2.0.0',
 'ipadic>=1.0.0,<2.0.0',
 'pytextspan>=0.5.4,<0.6.0',
 'tokenizers>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'japre',
    'version': '0.1.3',
    'description': 'Custom pretokenizers for Japanese language models',
    'long_description': '# japanese_pretokenizers (japre)\n\nCustom pretokenizers for Japanese language models\n\n## installation\n\n```\npip install japre\n```\n\n## Usage\n\n### IpadicPreTokenizer\n\n```python\nfrom japre.ipadic import IpadicPreTokenizer\n\nfrom transformers import PreTrainedTokenizerFast\nfrom tokenizers import Tokenizer\n\ntokenizer_object = Tokenizer.from_file("your-awesome-tokenizer.json")\ntokenizer_object.pre_tokenizer = IpadicPreTokenizer.make()\ntokenizer = PreTrainedTokenizerFast(\n    tokenizer_object=tokenizer_object,\n    unk_token=\'[UNK]\',\n    mask_token=\'[MASK]\',\n    cls_token=\'[CLS]\',\n    pad_token=\'[PAD]\',\n    sep_token=\'[SEP]\'\n)\n```\n\n### ManbyoDictPreTokenizer\n\n```\nexport MANBYO_DICT_PATH=/path/to/MANBYO_201907_Dic-utf8.dic\n```\n\n```python\nfrom japre.manbyo import ManbyoDictPreTokenizer\n\nfrom transformers import PreTrainedTokenizerFast\nfrom tokenizers import Tokenizer\n\ntokenizer_object = Tokenizer.from_file("your-awesome-tokenizer.json")\ntokenizer_object.pre_tokenizer = ManbyoDictPreTokenizer.make()\ntokenizer = PreTrainedTokenizerFast(\n    tokenizer_object=tokenizer_object,\n    unk_token=\'[UNK]\',\n    mask_token=\'[MASK]\',\n    cls_token=\'[CLS]\',\n    pad_token=\'[PAD]\',\n    sep_token=\'[SEP]\'\n)\n```',
    'author': 'Kaito Sugimoto',
    'author_email': 'kaito_sugimoto@is.s.u-tokyo.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Alab-NII/japanese_pretokenizers',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
