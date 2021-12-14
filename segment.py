from pyhanlp import *


class Segment:

    @classmethod
    def segment(cls, corpus_sentence):
        words = []
        for item in HanLP.segment(corpus_sentence):
            words.append({"word": item.word, "nature": str(item.nature)})
        return words
