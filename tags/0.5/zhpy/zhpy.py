#!/usr/bin/python
worddict = {"印出":"print", "輸入":"raw_input", #io

def merger(anno_dict):
        for tmp in anno_dict.keys:
            if not worddict.has_key(tmp):
                worddict[tmp] = anno_dict[tmp]
                print "add %s=%s"%(tmp, anno_dict[tmp])
