#!/usr/bin/env python2
import os

indexdir="echo/"
msgdir="msg/"

msgs = os.listdir(msgdir)
for h in msgs:
    if os.path.getsize('%s%s' % (msgdir,h) ) == 0:
        os.remove('%s%s' % (msgdir,h) )
        msgs.remove(h)

echoes = os.listdir(indexdir)

for ea in echoes:
    passed = []
    echo = open('%s%s' % (indexdir,ea) ).read().splitlines()
    for h in echo:
        if h in msgs:
            msgs.remove(h)
            passed.append(h)
    if passed != echo:
        passed = passed + [''] or []
        print ea
        open('%s%s' % (indexdir,ea),'w').write('\n'.join(passed))

for h in msgs:
    print h
    os.remove('%s%s' % (msgdir,h))
