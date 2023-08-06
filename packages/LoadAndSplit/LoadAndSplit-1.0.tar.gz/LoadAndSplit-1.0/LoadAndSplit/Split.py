from numpy import ndarray


def P(s, d: dict, arr: ndarray):
    """
    :param s: 词语，len(s) = 2
    :param d: token dict 汉字->数字
    :param arr: 【汉字1】【汉字2】=词语12在词库中的出现概率
    :return: 词语的出现概率
    """
    if s[0] in d and s[1] in d:
        return arr[d[s[0]]][d[s[1]]]
    else:
        return 0


def Split(text, d, arr):
    """
    :param text: 文本
    :param d: token dict 汉字->数字
    :param arr: 【汉字1】【汉字2】=词语12在词库中的出现概率
    :return: 分词后的list
    """
    i = 0
    cent = list(text)
    while i + 3 < len(cent):
        if P(cent[i:i + 2], d, arr) > P(cent[i + 1:i + 3], d, arr):
            cent.insert(i + 2, ' ')
            i += 3
        else:
            cent.insert(i + 1, ' ')
            i += 2
    return ''.join(cent).split(' ')
