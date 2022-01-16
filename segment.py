from pyhanlp import *


class Segment:
    def is_all_chinese(self, word):
        for i in word:
            if 'a' <= i <= 'z' or 'A' <= i <= 'Z':
                return False
        return True

    @classmethod
    def segment(cls, corpus):
        """
        基于HanLP的分词方法
        :param corpus: 语料数据
        :return: 分词后的词列表
        """
        words = []
        nature_filter = ["g", "gb", "gbc", "gc", "gg", "gi", "gm", "gp", "h", "i", "j", "k", "l", "n", "nb", "nba",
                         "nbc", "nbp", "nf", "ng", "nh", "nhd", "nhm", "ni", "nic", "nis", "nit", "nl", "nm", "nmc",
                         "nn", "nnd", "nnt", "nr", "nr1", "nr2", "nrf", "nrj", "ns", "nsf", "nt", "ntc", "ntcb", "ntcf",
                         "ntch", "nth", "nto", "nts", "ntu", "nx", "nz", "nz", "vn"]
        for item in HanLP.segment(corpus):
            if str(item.nature) in nature_filter and len(item.word) > 1 and cls().is_all_chinese(item.word):
                words.append(item.word)
        return words
