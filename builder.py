#!/usr/bin/env python3

from ii_functions import *
import os

check_dirs()

msgs = os.listdir(msgdir)
for h in msgs:
    if os.path.getsize(msgdir + h) == 0:
        delete(msgdir + h)
        msgs.remove(h)

echoes = os.listdir(indexdir)

for ea in echoes:
    passed = []
    echo = read_file(indexdir + ea).splitlines()
    for h in echo:
        if h in msgs:
            msgs.remove(h)
            passed.append(h)
    if passed != echo:
        passed = passed + [''] or []
        print(ea)
        open(indexdir + ea, 'w').write('\n'.join(passed))

for h in msgs:
    delete(msgdir + h)
