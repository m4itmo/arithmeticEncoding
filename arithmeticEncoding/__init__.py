from decimal import Decimal, getcontext
import logging


class ae:
    def __init__(self, number_of_signs: int = 1000, logging_level=logging.WARN, logging_filename: str = ''):
        getcontext().prec = number_of_signs
        if logging_filename:
            logging.basicConfig(level=logging_level, filename=logging_filename, filemode="w")
        else:
            logging.basicConfig(level=logging_level)

    def encode_dec(self, inp: str):
        inp += '\0'
        l = Decimal('0')
        r = Decimal('1')

        alp = sorted([{
            'letter': b,
            'repetitions': inp.count(b),
            'rate': Decimal(inp.count(b)) / Decimal(len(inp))
        } for b in list(set(list(inp)))], key=lambda x: [x['repetitions'], x['letter']], reverse=True)

        pre = Decimal('0')
        for letter in alp:
            letter['pre'] = pre
            pre += letter['rate']

        for letter in alp:
            logging.debug(letter)

        logging.debug('---')

        for letter in inp:
            for alpLetter in alp:
                if alpLetter['letter'] == letter:
                    logging.debug(alpLetter)
                    scale = r - l
                    l = alpLetter['pre'] * scale + l
                    r = l + alpLetter['rate'] * scale
                    break

            logging.debug(l)
            logging.debug(r)

        # return {'encoded': (r + l) / 2, 'aplh': alp}

        re = ''
        sl, sr = str(l), str(r)
        for i in range(min(len(sl), len(sr))):
            re += sr[i]
            if sl[i] != sr[i]:
                break

        return {'encoded': Decimal(re), 'aplh': alp}

    def decode_dec(self, inp: Decimal, alp):
        l = Decimal('0')
        r = Decimal('1')

        pre = Decimal('0')
        for letter in alp:
            letter['pre'] = pre
            pre += letter['rate']

        for letter in alp:
            logging.debug(letter)

        logging.debug('---')

        re = ''
        while True:
            scale = r - l
            logging.debug(f'#{scale}\t{l} {inp} {r}')
            for alpLetter in alp:
                logging.debug(alpLetter)
                logging.debug(f"{alpLetter['pre'] * scale + l} {inp} "
                              f"{l + alpLetter['pre'] * scale + alpLetter['rate'] * scale} {alpLetter['letter']}")
                if alpLetter['pre'] * scale + l <= inp <= l + alpLetter['pre'] * scale + alpLetter['rate'] * scale:
                    l = alpLetter['pre'] * scale + l
                    r = l + alpLetter['rate'] * scale
                    if alpLetter['letter'] == '\0':
                        return {'decoded': re, 'aplh': alp}
                    re += alpLetter['letter']
                    logging.debug('+= ' + alpLetter['letter'])
                    break

            logging.debug(l)
            logging.debug(r)
