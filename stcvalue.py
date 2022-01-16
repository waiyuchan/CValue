import csv
import codecs
from itertools import islice


class STCValue(object):
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.terms_dicts = self.terms_reader()
        self.terms_dicts = self.terms_extraction()
        self.terms_export()

    def terms_reader(self):
        """
        :return: 从csv中读取的候选术语合集（词名 & 词频 & c-value值） {"terms":{"frequency":(int), "cvalue:(float)}}
        """

        if self.input_file.endswith(".csv"):
            csv.field_size_limit(500 * 1024 * 1024)
            csv_reader = csv.reader(codecs.open(self.input_file, "r"))
            terms_dicts = {}
            for item in islice(csv_reader, 1, None):
                terms_dicts[item[0]] = {"frequency": int(item[1]), "cvalue": float(item[2]),
                                        "finish": False, "hs": set(), "ts": set()}
            return terms_dicts
        else:
            raise TypeError

    def terms_extraction(self):
        """
        复现核心算法,完成STC-value计算的候选术语集合
        :return:
        """
        terms_dicts = self.terms_dicts
        for term in terms_dicts.keys():
            terms_dicts[term]["finish"] = True
            for other_term in terms_dicts.keys():
                if terms_dicts[other_term]["finish"]:
                    continue
                for index in range(min(len(term), len(other_term))):
                    if index == min(len(term), len(other_term))-1 and term[index] == other_term[index]:
                        terms_dicts[term]["hs"].add(other_term)
                        terms_dicts[other_term]["hs"].add(term)
                    if term[index] != other_term[index]:
                        if index > 1:
                            terms_dicts[term]["hs"].add(other_term)
                            terms_dicts[other_term]["hs"].add(term)
                        break
                for index in range(1, min(len(term), len(other_term))+1):
                    if index == min(len(term), len(other_term)) and term[-index] == other_term[-index]:
                        terms_dicts[term]["ts"].add(other_term)
                        terms_dicts[other_term]["ts"].add(term)
                    if term[-index] != other_term[-index] or index == min(len(term), len(other_term)):
                        if index > 2:
                            terms_dicts[term]["ts"].add(other_term)
                            terms_dicts[other_term]["ts"].add(term)
                        break
        a = 0.2
        for term in terms_dicts.keys():  # 计算stc-value的值
            hw = (len(terms_dicts[term]["hs"])+1)/len(terms_dicts.keys())
            tw = (len(terms_dicts[term]["ts"])+1)/len(terms_dicts.keys())
            hs_ans = 0
            ts_ans = 0
            for i in terms_dicts[term]["hs"]:
                hs_ans += terms_dicts[i]["cvalue"]
            for i in terms_dicts[term]["ts"]:
                ts_ans += terms_dicts[i]["cvalue"]
            terms_dicts[term]["stcvalue"] = (1-a)*terms_dicts[term]["cvalue"]+a*(hw*hs_ans+tw*ts_ans)

        return terms_dicts

    def terms_export(self):
        """
        导出候选术语集合到文件
        :return:None
        """
        candidate_terms = []
        for candidate_term in self.terms_dicts:
            candidate_term_frequency = self.terms_dicts[candidate_term]["frequency"]
            candidate_term_stcvalue = self.terms_dicts[candidate_term]["stcvalue"]
            candidate_term_cvalue = self.terms_dicts[candidate_term]["cvalue"]
            candidate_term_hs = "/".join(list(self.terms_dicts[candidate_term]["hs"]))
            candidate_term_ts = "/".join(list(self.terms_dicts[candidate_term]["ts"]))
            candidate_terms.append([candidate_term, candidate_term_frequency, candidate_term_stcvalue,
                                    candidate_term_cvalue, candidate_term_hs, candidate_term_ts])
        with open(self.output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["术语", "词频", "STC-value", "C-value", "头部相似候选术语集", "尾部相似候选术语集"])
            for item in candidate_terms:
                writer.writerow(item)

