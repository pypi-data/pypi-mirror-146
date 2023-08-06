from fugashi import GenericTagger
import ipadic

from .ipadic import IpadicPreTokenizer


def try_load_manbyo_dict_path():
    try:
        import os
        MANBYO_DICT_PATH = os.environ["MANBYO_DICT_PATH"]
        return MANBYO_DICT_PATH
    except Exception as e:
        print(e)


class ManbyoDictTagger(GenericTagger):
    """
    fugashi with ipadic and manbyo dictionaries
    """
    MANBYO_DICT_PATH = try_load_manbyo_dict_path()

    MECAB_ARGS = ' '.join([ipadic.MECAB_ARGS, '-u ' + MANBYO_DICT_PATH])

    def __init__(self):
        super().__init__(self.MECAB_ARGS)


class ManbyoDictPreTokenizer(IpadicPreTokenizer):
    """
    PreTokenizer with CustomTagger
    Note that, since this PreTokenizer is not serializable,
    we have to load model and pretokenizer separately.
    """

    def __init__(self):

        self.tagger = ManbyoDictTagger()
