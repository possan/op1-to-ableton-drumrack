import chunk
import json
import os.path
import random
import glob
import sys
import gzip


def readTemplate(fn):
    f = open (fn)
    s = f.read()
    f.close()
    return s

DRUMRACK_ROOT_TEMPLATE = readTemplate('drumrack-root-template.xml')
DRUMRACK_SAMPLER_TEMPLATE = readTemplate('drumrack-sampler-template.xml')


def getOP1chunk(fi):
    ret = None
    f2 = open(fi, 'rb')
    d = f2.read(4)
    if d != b'FORM':
        return None
    d = f2.read(4)
    d = f2.read(4)
    if d != b'AIFF' and d != b'AIFC':
        return None
    for k in range(10):
        try:
            c = chunk.Chunk(f2)
            print ("chunk %s, %d bytes" % (c.getname(), c.getsize()))
            if c.getname() == b'APPL':
                f4 = c.read(4)
                if f4 == b'op-1':
                    s = c.read(c.getsize() - 4)
                    s = s.decode('utf-8').strip('\0').strip()
                    j = json.loads(s)
                    ret = j
            c.skip()
        except EOFError:
            pass
    f2.close()
    return ret

def writeDrumRackPatch(fi, config, fo, audiofilename):
    samplers = ''

    num = len(config['start'])
    for k in range(num):
        idx = (num - 1) - k
        st = round(0 + config['start'][k] / 4096)
        en = round(0 + config['end'][k] / 4096)

        x = DRUMRACK_SAMPLER_TEMPLATE
        x = x.replace('{name}', 'Seg ' + str(k))
        x = x.replace('{note}', str(69 + idx))
        x = x.replace('{audiofilename}', audiofilename)
        x = x.replace('{samplestart}', str(st))
        x = x.replace('{sampleend}', str(en))
        samplers += x

    x = DRUMRACK_ROOT_TEMPLATE
    x = x.replace('{samplers}', samplers)
    x = x.replace('{filename}', audiofilename)

    with gzip.open(fo, 'wb') as f:
        f.write(x.encode('utf-8'))

def convert(fi, patchout):
    ch = getOP1chunk(fi)
    if ch == None:
        print ("Not an OP-1 audio file.")
        return
    print ("OP-1 Chunk: %r" % (ch))
    audiofilename = os.path.splitext(os.path.basename(patchout))[0] + '.aif'
    if ch['type'] == 'drum':
        writeDrumRackPatch(fi, ch, patchout, audiofilename)
    else:
        print("Unknown device type.")

if len(sys.argv) < 2:
    print('Syntax: python3 convert.py "downloaded/*.aif"')
    sys.exit(1)

files = glob.iglob(sys.argv[1], recursive=True)
for aiffilepath in files:
    print("AIF File " + aiffilepath)
    adgfilename = os.path.splitext(os.path.basename(aiffilepath))[0] + '.adg'
    adgfilepath = os.path.join(os.path.dirname(aiffilepath), adgfilename)
    print("ADG File path " + adgfilepath)
    if not os.path.exists(adgfilepath):
        convert(aiffilepath, adgfilepath)
