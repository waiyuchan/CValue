import math
import csv

from itertools import islice
from segment import Segment
import codecs


class PCValue(object):

    def __init__(self, input_file, output_file):
        """
        初始化方法
        :param input_file: 输入文件
        :param output_file: 输出文件
        """
        self.input_file = input_file
        self.output_file = output_file
        self.corpus, self.textlist = self.corpus_input()
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
                    if "nested" not in candidate_terms_list[i]:
                        candidate_terms_list[i]["nested"] = {}
                    candidate_terms_list[i]["nested"][j] = candidate_terms_list[j]["frequency"]

        for term in candidate_terms_list:
            text_frequency = 0
            for text in self.textlist:
                if term in text:
                    text_frequency += 1
            if "nested" in candidate_terms_list[term]:
                nested_terms = candidate_terms_list[term]["nested"]
                nested_size = len(nested_terms)
                nested_frequency = 0
                for nested_item in nested_terms:
                    nested_frequency += nested_terms[nested_item]
                    # print(nested_item)
                    # print(candidate_terms_list)
                    if "nested" in candidate_terms_list[nested_item]:
                        for i in candidate_terms_list[nested_item]["nested"]:
                            nested_frequency -= candidate_terms_list[i]["frequency"]

                candidate_terms_list[term]["pcvalue"] = self.c_value_algorithm(length=len(term),
                                                                              text_frequency=text_frequency,
                                                                              frequency=candidate_terms_list[term][
                                                                                  "frequency"],
                                                                              nested_size=nested_size,
                                                                              nested_frequency=nested_frequency)
            else:
                candidate_terms_list[term]["pcvalue"] = self.c_value_algorithm(length=len(term),
                                                                              text_frequency=text_frequency,
                                                                              frequency=candidate_terms_list[term][
                                                                                  "frequency"])

        return candidate_terms_list

    def c_value_algorithm(self, length, text_frequency, frequency, nested_size=None, nested_frequency=None):
        """
        C-value 算法实现
        :param length: 候选术语长度
        :param frequency: 候选术语词频
        :param nested_size: 嵌套该候选术语的候选术语数量
        :param nested_frequency: 被嵌套的总次数
        :return:
        """
        if nested_size is None:
            pcvalue = math.log2(length) * frequency + math.pow(2, length-2)*text_frequency
            return pcvalue
        else:
            pcvalue = math.log2(length) * (frequency - (1 / nested_size) * nested_frequency) \
                     + math.pow(2, length-2) * text_frequency
            return pcvalue

    def corpus_input(self):
        """
        语料数据导入处理，转为字符串数据
        :return: 字符串格式的语料数据
        """
        corpus = ""
        if self.input_file.endswith(".csv"):
            csv.field_size_limit(500 * 1024 * 1024)
            csv_reader = csv.reader(codecs.open(self.input_file, "r", "utf-8"))
            '''
            for item in islice(csv_reader, 1, None):
                s = ""
                for i in item:
                    s += " {} ".format(str(i))
                corpus += s
            print(corpus)
            '''
            column = [row[9] for row in csv_reader]
            # print(column)
            # print(type(csv_reader), type(column))
            corpus = " "+" ".join(column[1:])
            # print(corpus)

        elif self.input_file.endswith(".txt"):
            with open(self.input_file, "r") as f:
                corpus = f.read()
        else:
            raise TypeError
        return corpus, column

    def terms_export(self):
        """
        导出候选术语集合到文件
        :return: None
        """
        candidate_terms = []
        for candidate_term in self.candidate_terms_list:
            candidate_term_frequency = self.candidate_terms_list[candidate_term]["frequency"]
            candidate_term_pcvalue = self.candidate_terms_list[candidate_term]["pcvalue"]
            if "nested" in self.candidate_terms_list[candidate_term]:
                candidate_term_nested = str(self.candidate_terms_list[candidate_term]["nested"])
            else:
                candidate_term_nested = None
            candidate_terms.append([candidate_term, candidate_term_frequency, candidate_term_pcvalue, candidate_term_nested])
        with open(self.output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["术语", "词频", "PC-value", "nested"])
            for item in candidate_terms:
                writer.writerow(item)
