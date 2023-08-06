from collections import Counter

from numpy import zeros, int32, float64, ndarray


def Load(raw_text: str) -> tuple[dict, ndarray]:
    """
    :param raw_text: 语料库，句子间以换行分割
    :return: tuple(dict, numpy.ndarray)
    dict: token 汉字->数字
    numpy.ndarray 【汉字1】【汉字2】=词语12在词库中的出现概率
    """
    count = Counter(raw_text)
    count.pop('\n')
    N = len(count)

    arr = zeros(shape=(N, N), dtype=float64)
    arr1 = zeros(shape=(N,), dtype=int32)

    d = {}
    i = 0
    for k in count:
        d[k] = i
        i += 1

    for cen in raw_text.split('\n'):
        t1 = cen[:-2]
        t2 = cen[1:-1]
        for a, b in zip(t1, t2):
            arr1[d[a]] += 1
            arr[d[a]][d[b]] += 1
    for i in range(N):
        arr[i] = arr[i] / (arr1[i] if arr1[i] else 1)

    return d, arr
