from fugashi import GenericTagger
import ipadic
import textspan
import tokenizers


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
