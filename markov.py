'''
This is the Markov module. This is docstring for the module

>>> m = Markov('ab')
>>> m.predict('a')
'b'

'''
import argparse
import random
import sys
import urllib.request as req

def fetch_url(url, fname):
    'get contents of url put in fname'
    fin = req.urlopen(url)
    data = fin.read()
    with open(fname, mode='wb') as fout:
        fout.write(data)
    #context mgr closes file


def from_file(fname, size=1, encoding='utf8'):
    with open(fname, encoding=encoding) as fin:
        txt = fin.read()
    return Markov(txt, size=size)


class Markov:
    def __init__(self, txt, size=1):
        self.tables =[]
        for i in range(size):
            self.tables.append(get_table(txt, size=i+1))

    def predict(self, txt):
        #options = self.table.get(txt,{})
        table = self.tables[len(txt)-1]
        options = table.get(txt, {})
        if not options:
            raise KeyError(f'{txt} not found')
        possibles = []
        for key in options:
            count = options[key]
            for i in range(count):
                possibles.append(key)
        return random.choice(possibles)


def get_table(txt, size=1):
    results ={}
    for i in range(len(txt)):
        chars = txt[i:i+size]
        try:
            out = txt[i+size]
        except IndexError:
            break
        char_dict = results.get(chars, {})
        char_dict.setdefault(out,0)
        char_dict[out] += 1

        results[chars] = char_dict
    return results


def repl(m):
    print("Welcome to the Markov REPL. (Hit Ctl-C to exit)")
    while True:
        try:
            txt = input('>')
        except KeyboardInterrupt:
            print("Goodbye")
            break
        try:
            res = m.predict(txt)
        except KeyError:
            print("Word not found")
        except IndexError:
            print('Try again')
        else:
            print(res)

def main(args):
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', help='input file')
    ap.add_argument('-s', '--size', help='Markov size',
                    default=1, type=int)
    opts = ap.parse_args(args)
    if opts.file:
        m = from_file(opts.file, size=opts.size)
        repl(m)


if __name__ == '__main__':
    main(sys.argv[1:])
        
