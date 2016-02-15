#!/usr/bin/env python3

import os
from ii_functions import *

check_dirs()

msgs = os.listdir(msgdir)
passed = set()

echoes = os.listdir(indexdir)

for ea in echoes:
    for h in read_file(indexdir + ea).splitlines():
        if h in msgs:
            msgs.remove(h)
            passed.add(h)
        else:
            if h in passed:
                print('double in %s: %s' % (ea, h))
            else:
                print('bad record in %s: "%s"' % (ea, h))

for h in msgs:
    print('no owner for %s' % h)
