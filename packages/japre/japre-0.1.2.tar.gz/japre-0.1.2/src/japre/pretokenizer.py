from fugashi import GenericTagger
import ipadic
import textspan
import tokenizers


def try_load_manbyo_dict_path():
    try:
        import os
        MANBYO_DICT_PATH = os.environ["MANBYO_DICT_PATH"]
        return MANBYO_DICT_PATH
    except Exception as e:
        print(e)


#
# Pretokenizers for Japanese sequences
#
class IpadicTagger(GenericTagger):
    """
    fugashi with ipadic
    """
    def __init__(self):
        super().__init__(ipadic.MECAB_ARGS)


class IpadicPreTokenizer(object):
    """
    PreTokenizer with IpadicTagger
    Note that, since this PreTokenizer is not serializable,
    we have to load model and pretokenizer separately.
    """

    @classmethod
    def make(cls):
        """instantiate a PreTokenizer object."""
        return tokenizers.pre_tokenizers.PreTokenizer.custom(cls())

    def __init__(self):

        self.tagger = IpadicTagger()

    def _pre_tokenize(self, _id, ns):

        text = ns.normalized
        tokens = [n.surface for n in self.tagger.parseToNodeList(text)]
        tokens_spans = textspan.get_original_spans(tokens, text)
        return [ns[sp:ep] for sub_spans in tokens_spans for sp, ep in sub_spans]

    def pre_tokenize(self, pretok):

        pretok.split(self._pre_tokenize)


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
