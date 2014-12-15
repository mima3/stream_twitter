# -*- coding: utf-8 -*-
import sys
import codecs
from twitter_db import *
reload(sys)
sys.setdefaultencoding('utf-8')
import MeCab
from collections import defaultdict


def main(argvs, argc):
    if argc != 3:
        print ("Usage #python %s start_date end_date interval_sec" % argvs[0])
        return 1
    start_date = argvs[1]
    end_date = argvs[2]

    mecab = MeCab.Tagger('')
    tweets = GetTwittes(start_date, end_date)
    pos = [u'名詞',u'形容詞', u'形容動詞',u'感動詞',u'動詞',u'副詞'] #u'形容詞', u'形容動詞',u'感動詞',u'副詞',u'連体詞',u'名詞',u'動詞']
    exclude=[
      u'RT',
      u'TL',
      u'sm',
      u'#',
      u'さん',
      u'ある',
      u'する',
      u'いる',
      u'やる',
      u'これ',
      u'それ',
      u'あれ',
      '://',
      u'こと',
      u'の',
      u'そこ',
      u'ん',
      u'なる',
      u'http',
      u'https',
      u'co',
      u'jp',
      u'com'
    ]
    wordcount = defaultdict(int)
    for tweet in tweets:
        txt = tweet.contents.encode('utf-8')
        node = mecab.parseToNode(txt)
        while node:
            fs = node.feature.split(",")
            if fs[0] in pos:
                word = (fs[6] != '*' and fs[6] or node.surface)
                word = word.strip()
                if word.isdigit() == False:
                    if len(word)!=1:
                        if word not in exclude:
                            wordcount[word] += 1
            node = node.next

    for k, v in sorted(wordcount.items(), key=lambda x:x[1], reverse=True):
        if v == 1:
            break
        print ("%s\t%d" % (k, v))

if __name__ == '__main__':
    #sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout, errors='backslashreplace')
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
