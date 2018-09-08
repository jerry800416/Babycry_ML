# -*- coding:utf-8 -*-

import os

class ImageRename():
    def __init__(self):
        self.path = './testdata/cel'

    def rename(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)
  
        i = 0

        for item in filelist:
            src = os.path.join(os.path.abspath(self.path), item)
            dst = os.path.join(os.path.abspath(self.path), 'cel'+ format(i) + '.wav')
            os.rename(src, dst)
            print('converting {} to {} ...'.format(src, dst))
            i = i + 1
            print('total {} to rename & converted {} wavs'.format(total_num, i))

if __name__ == '__main__':
    newname = ImageRename()
    newname.rename()