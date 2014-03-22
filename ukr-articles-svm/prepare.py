#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def readfile(filename):
    with open(filename) as f:
        return f.read().decode('utf8').replace(u'\n', u' ')


def canonize(source):
    stop_symbols = u'.,!?:;-\n\r()'
    stop_words = (u'это', u'как', u'так', u'и', u'в', u'над', u'к', u'до', u'не', u'на', u'но', u'за', u'то', u'с', u'об', u'по', u'—', u'из',
        u'ли', u'а', u'во', u'от', u'со', u'для', u'о', u'же', u'ну', u'вы', u'бы', u'что', u'кто', u'он', u'она', u'этом', u'также', u'его')
    return ([x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)])


def get_freq(filename):
    words = canonize(readfile(filename))
    check = list(set(words))
    for w in check:
        yield w, words.count(w)


def get_top_freq(files):
    words = []
    for f, c in files:
        words.extend(list(get_freq(f)))
    words.sort(key=lambda x: x[0])

    w = None
    s = 0
    ss = 0
    res = []
    for cw, f in words:
        ss += s
        if cw != w:
            if w is not None:
                res.append((w, ss))
            w = cw
            ss = 0
        s = f

    # words.sort(key=lambda x: x[1])
    words = sorted(res, key=lambda x: x[1])
    return list(reversed(words))[:20]


def calc_freq(words, freqs):
    for w, f in freqs:
        print w, words.count(w)
        yield words.count(w)


def prepare(filename, is_ukr, freqs):
    print "\ntext", filename
    words = canonize(readfile(filename))
    ft = list(calc_freq(words, freqs))
    string = '%i' % is_ukr
    for i in xrange(len(ft)):
        string += ' %i:%f' % (i + 1, ft[i])
    return string


def create_dataset(files, freqs, filename):
    with open(filename, "w") as f:
        for ff, c in files:
            f.write(prepare(ff, c, freqs) + '\n')


def save_freqs(freqs, filename):
    with open(filename, "w") as f:
        f.write(json.dumps(freqs))


def main():
    files = [('arts/u1', True), ('arts/u2', True), ('arts/u3', True), ('arts/u4', True), ('arts/u5', True),
    ('arts/o1', False), ('arts/o2', False), ('arts/o3', False), ('arts/o4', False), ('arts/o5', False)]
    files2 = [('arts/to1', False), ('arts/tu1', True)]
    freqs = get_top_freq(files)

    print 'freqs'
    for w, f in freqs:
        print w, f

    create_dataset(files, freqs, 'dataset')
    create_dataset(files2, freqs, 'testset')
    save_freqs(freqs, "features")


if __name__ == '__main__':
    main()
