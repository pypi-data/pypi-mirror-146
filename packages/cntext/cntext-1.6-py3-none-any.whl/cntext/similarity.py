#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import Differ, SequenceMatcher
import jieba
#from math import *
import warnings

warnings.filterwarnings('ignore')


def __check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def __transform(text1, text2):
    """
    把文本text1，text2转化为英文样式的text1，text2和向量vec1，vec2
    :param text1:
    :param text2:
    :return:
    """

    if __check_contain_chinese(text1):
        text1 = ' '.join(jieba.lcut(text1))
        text2 = ' '.join(jieba.lcut(text2))
    else:
        text1 = text1.lower()
        text2 = text2.lower()

    corpus = [text1, text2]
    cv = CountVectorizer(binary=True)
    cv.fit(corpus)
    vec1 = cv.transform([text1]).toarray()
    vec2 = cv.transform([text2]).toarray()
    return text1, text2, vec1, vec2


#def cosine_similarity(vec1, vec2):
#    cos_sim = cosine_similarity(vec1, vec2)[0][0]
#    return cos_sim[0][0]

def jaccard_sim(text1, text2):
    """
    jaccard相似度算法; 
    :param text1:  文本字符串
    :param text2: 文本字符串
    :return:  返回相似度数值结果
    """
    text11, text22, vec1, vec2 = __transform(text1, text1)
    """ returns the jaccard similarity between two lists """
    vec1 = set([idx for idx, v in enumerate(vec1[0]) if v > 0])
    vec2 = set([idx for idx, v in enumerate(vec2[0]) if v > 0])
    return len(vec1 & vec2) / len(vec1 | vec2)

def minedit_sim(text1, text2):
    """
    最小编辑距离相似度算法； 
    :param text1:  文本字符串
    :param text2: 文本字符串
    :return:  返回相似度数值结果
    """
    words1 = jieba.lcut(text1.lower())
    words2 = jieba.lcut(text2.lower())
    leven_cost = 0
    s = SequenceMatcher(None, words1, words2)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'replace':
            leven_cost += max(i2 - i1, j2 - j1)
        elif tag == 'insert':
            leven_cost += (j2 - j1)
        elif tag == 'delete':
            leven_cost += (i2 - i1)
    return leven_cost


def simple_sim(text1, text2):
    """
    更改变动算法。
    参考微软word中的track change函数和Unix系统中的diff函数。
    :param text1:  文本字符串
    :param text2: 文本字符串
    :return:  返回相似度数值结果
    """
    words1 = jieba.lcut(text1.lower())
    words2 = jieba.lcut(text2.lower())
    diff = Differ()
    diff_manipulate = list(diff.compare(words1, words2))
    c = len(diff_manipulate) / (len(words1) + len(words2))
    cmax = max([len(words1), len(words2)])
    return (cmax - c) / cmax


def cosine_sim(text1, text2):
    """
    对输入的text1和text2进行相似性计算，返回相似性信息
    :param text1:  文本字符串
    :param text2: 文本字符串
    :return:  返回相似度数值结果
    """
    text11, text22, vec1, vec2 = __transform(text1, text1)
    return cosine_similarity(vec1, vec2)[0][0]
