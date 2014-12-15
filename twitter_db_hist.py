# -*- coding: utf-8 -*-
# easy_install python_twitter
import twitter
import sys
import codecs
from twitter_db import *
import matplotlib.pyplot as plt


def main(argvs, argc):
    if argc != 4:
        print ("Usage #python %s start_date end_date interval_sec" % argvs[0])
        return 1
    start_date = argvs[1]
    end_date = argvs[2]
    interval_sec = argvs[3]
    tweets = GetTwitteHistogram(start_date, end_date, interval_sec)
    x = []
    y = []
    label = []
    i = 1
    for tweet in tweets:
        print ("%s\t%s" % (tweet[0], tweet[1]))
        if i == 1 or i == len(tweets):
            label.append(tweet[0])
        else:
            label.append('')
        y.append(tweet[1])
        x.append(i)
        i = i + 1
    plt.bar(x,y)
    plt.xticks(x, label)
    plt.show()

    #for tweet in tweets:
    #    print tweet.createAt
    #    print tweet.contents

if __name__ == '__main__':
    sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout, errors='backslashreplace')
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
