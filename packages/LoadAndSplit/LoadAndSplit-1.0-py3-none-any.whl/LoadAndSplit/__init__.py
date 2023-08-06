from pickle import load

from LoadAndSplit.Load import Load
from LoadAndSplit.Split import Split, P


class Model:
    def __init__(self, raw):
        """
        :param raw: 语料库，句子间以换行分割
        """
        self.token, self.PArray = Load(raw)

    def split(self, text):
        """
        :param text: 文本
        :return: 分词后的list
        """
        return Split(text, self.token, self.PArray)

    def wordProbability(self, text):
        """
        :param text: 词语，len(text) = 2
        :return: 词语的出现概率
        """
        return P(text, self.token, self.PArray)

    def __repr__(self):
        return '<zh-cn word split Model>'


def FromRaw(text: str) -> Model:
    """

    :param text: 语料库，句子间以换行分割
    :return: Model(text)
    """
    return Model(text)


def Default_Model():
    from os.path import join
    from os import getcwd
    print(join('Default_Model.pkl', getcwd()))
    with open(__path__[0]+'\\Default_Model.pkl', 'rb') as f:
        return load(f)
