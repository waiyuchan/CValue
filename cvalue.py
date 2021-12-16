import math
import csv

from itertools import islice
from segment import Segment


class CValue(object):

    def __init__(self, input_file, output_file):
        """
        初始化方法
        :param input_file: 输入文件
        :param output_file: 输出文件
        """
        self.input_file = input_file
        self.output_file = output_file
        self.corpus = self.corpus_input()
        self.candidate_term_count = 0
        self.candidate_terms_list = self.terms_extraction()
        self.terms_export()

    def terms_extraction(self):
        """
        术语抽取核心方法
        :return: 完成C-value计算的候选术语集合
        """
        candidate_terms = Segment.segment(self.corpus)
        self.candidate_term_count = len(candidate_terms)
        candidate_terms_list = {}
        for term in candidate_terms:
            if term not in candidate_terms_list.keys():
                candidate_terms_list[term] = {"frequency": 1}
            else:
                candidate_terms_list[term]["frequency"] += 1
        candidate_term_keys = candidate_terms_list.keys()
        for i in candidate_term_keys:
            for j in candidate_term_keys:
                if i != j and i in j:
                    candidate_terms_list[i]["nested"] = {j: candidate_terms_list[j]["frequency"]}

        for term in candidate_terms_list:
            if "nested" in candidate_terms_list[term]:
                nested_terms = candidate_terms_list[term]["nested"]
                nested_size = len(nested_terms)
                nested_frequency = 0
                for nested_item in nested_terms:
                    nested_frequency += nested_terms[nested_item]
                candidate_terms_list[term]["cvalue"] = self.c_value_algorithm(length=len(term),
                                                                              frequency=candidate_terms_list[term][
                                                                                  "frequency"],
                                                                              nested_size=nested_size,
                                                                              nested_frequency=nested_frequency)
            else:
                candidate_terms_list[term]["cvalue"] = self.c_value_algorithm(length=len(term),
                                                                              frequency=candidate_terms_list[term][
                                                                                  "frequency"])

        return candidate_terms_list

    def c_value_algorithm(self, length, frequency, nested_size=None, nested_frequency=None):
        """
        C-value 算法实现
        :param length: 候选术语长度
        :param frequency: 候选术语词频
        :param nested_size: 嵌套该候选术语的候选术语数量
        :param nested_frequency: 被嵌套的总次数
        :return:
        """
        if nested_size is None:
            cvalue = math.log2(length) * frequency
            return cvalue
        else:
            cvalue = math.log2(length) * (frequency - 1 / nested_size) * nested_frequency
            return cvalue

    def corpus_input(self):
        """
        语料数据导入处理，转为字符串数据
        :return: 字符串格式的语料数据
        """
        corpus = ""
        if self.input_file.endswith(".csv"):
            csv_reader = csv.reader(open(self.input_file))
            for item in islice(csv_reader, 1, None):
                s = ""
                for i in item:
                    s += " {} ".format(str(i))
                corpus += s
        elif self.input_file.endswith(".txt"):
            with open(self.input_file, "r") as f:
                corpus = f.read()
        else:
            raise TypeError
        return corpus

    def terms_export(self):
        """
        导出候选术语集合到文件
        :return: None
        """
        candidate_terms = []
        for candidate_term in self.candidate_terms_list:
            candidate_term_frequency = self.candidate_terms_list[candidate_term]["frequency"]
            candidate_term_cvalue = self.candidate_terms_list[candidate_term]["cvalue"]
            candidate_terms.append([candidate_term, candidate_term_frequency, candidate_term_cvalue])
        with open(self.output_file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["术语", "词频", "C-value"])
            for item in candidate_terms:
                writer.writerow(item)
