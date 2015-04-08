#!/usr/bin/env python2
import os

indexdir="echo/"
msgdir="msg/"

msgs = os.listdir(msgdir)
passed = set()

echoes = os.listdir(indexdir)

for ea in echoes:
    for h in open('%s%s' % (indexdir,ea) ).read().splitlines():
        if h in msgs:
            msgs.remove(h)
            passed.add(h)
        else:
            if h in passed:
                print 'double in %s: %s' % (ea, h)
            else:
                print 'bad record in %s: "%s"' % (ea, h)

for h in msgs:
    print 'no owner for %s' % h
