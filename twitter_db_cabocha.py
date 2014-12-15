# -*- coding: utf-8 -*-
import sys
import codecs
import re
from twitter_db import *
reload(sys)
sys.setdefaultencoding('utf-8')
from cabocha_ex import CaboChaEx
from collections import defaultdict


def main(argvs, argc):
    if argc != 3:
        print ("Usage #python %s start_date end_date interval_sec" % argvs[0])
        return 1
    start_date = argvs[1]
    end_date = argvs[2]

    cabocha = CaboChaEx("")
    tweets = GetTwittes(start_date, end_date)
    result = defaultdict(int)
    for tweet in tweets:
        sentences=re.split(u'[／”「」!?！？。.｢｣]' , tweet.contents)
        for t in sentences:
            if t == "":
                continue
            cabocha.parse(t.encode('utf-8'))
            ret = cabocha.pair()
            for k in ret.keys():
                key = k + "->" + ret[k]
                result[key] += 1
    for k1, d1 in sorted(result.items(), key=lambda x:x[1], reverse=True):
        print ("%s\t%d" % (k1, d1))

if __name__ == '__main__':
    #sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout, errors='backslashreplace')
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
