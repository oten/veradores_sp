#!/usr/bin/env python
#coding: utf-8
import sys
import json
import codecs

if __name__ == "__main__":
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    
    sys.stdout.write(json.dumps(json.loads(sys.stdin.read()), indent=4, separators=(',', ': '), ensure_ascii=False))
