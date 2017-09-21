# -*- coding: utf-8 -*-
Image = None
from PIL import Image as i
import wcwidth
Image = i
import sys
import os, platform

class QRCode():        
    def showCmdQRCode(self, filename):
        global Image
        import wcwidth
        # 165x165 -> 33x33
        size=33
        padding=1
        rgb=Image.open(filename).resize((size,size)).convert('RGB')
    
        qrtext = '0' * (size + padding * 2) + '\n'
        for rr in range(size):
            qrtext += '0'*padding
            for cc in range(size):
                r,g,b = rgb.getpixel((cc,rr))
                if (r > 127 or g > 127 or b > 127):
                    qrtext += '0'
                else:
                    qrtext += '1'
            qrtext += '0'*padding
            qrtext += '\n'
        qrtext = qrtext + '0' * (size + padding * 2) + '\n'

        try:
            b = u'\u2588'
            sys.stdout.write(b + '\r')
            sys.stdout.flush()
        except UnicodeEncodeError:
            white = 'MM'
        else:
            white = b
        
        black='  '
    
        # currently for Windows, '\u2588' is not correct. So use 'MM' for windows.
        osName = platform.system()
        if osName == 'Windows':
            white = '@@'

        blockCount = int(2/wcwidth.wcswidth(white))
        white *= abs(blockCount)

        sys.stdout.write(' '*50 + '\r')
        sys.stdout.flush()
        qr = qrtext.replace('0', white).replace('1', black)
        qr = '\033[37m\033[40m\n' + qr + '\033[0m\n' # force to use white/black.
        sys.stdout.write(qr)
        sys.stdout.flush()

        if os.path.exists(filename):
            os.remove(filename)
'''
    # A space-saving text QRCode
    if osName != 'Windows':
        charlist = [u' ',      u'\u2598', u'\u259D', u'\u2580', u'\u2596', u'\u258C', u'\u259E', u'\u259B',
                    u'\u2597', u'\u259A', u'\u2590', u'\u259C', u'\u2584', u'\u2599', u'\u259F', u'\u2588']
        qrarray = map(lambda x: map(lambda y: y, x), qrtext.split('\n'))
        qrtext = ''
        for rr in range(0, size + padding * 2, 2):
            for cc in range(0, size + padding * 2, 2):
                index = int(''.join([x for row in qrarray[rr:rr+2] for x in (row + ['0'])[cc:cc+2]][::-1]), 2)
                qrtext += hex(15 - index)[-1]
            qrtext += '\n'
        qr = ''.join(map(lambda x: charlist[int(x, 16)] if x != '\n' else x, qrtext))
        qr = '\033[37m\033[40m\n' + qr + '\033[0m\n'  # force to use white/black.
        sys.stdout.write(qr)
        sys.stdout.flush()
'''
#if __name__ == '__main__':
#    showCmdQRCode('qr.png')
