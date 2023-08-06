class ChileanCI(object):
    def __init__(self, ci):
        self.ci = str(ci)
        self.vd = None
        self.clean()

    def clean(self):
        self.ci = self.ci.strip().replace(' ', '')
        if '-' in self.ci:
            ci_tmp = self.ci.split('-')
            self.ci = ci_tmp[0]
            self.vd = ci_tmp[1].upper()
        self.ci = self.ci.replace('.', '')
        if len(self.ci) < 7 or len(self.ci) > 8:
            raise ValueError('Invalid length')
        if len(self.ci) < 8:
            for i in range(len(self.ci), 8):
                self.ci = '0' + self.ci

    def get_validation_digit(self):
        reversed_digits = map(int, reversed(self.ci))
        factors = [2, 3, 4, 5, 6, 7, 2, 3]
        s = sum(d * f for d, f in zip(reversed_digits, factors))
        vd = 'K' if (-s) % 11 == 10 else (-s) % 11
        return vd

    def is_valid(self):
        if self.vd is None:
            raise ValueError('No validation digit')
        return self.vd == self.get_validation_digit()

    def format(self, with_dashes=True, with_dots=True, vd=None):
        ci = list(str(int(self.ci)))
        if with_dashes:
            if with_dots:
                ci.insert(len(ci) - 3, '.')
                ci.insert(len(ci) - 7, '.')
            ci.append('-')
        if not vd:
            vd = self.vd if self.vd else str(self.get_validation_digit())
        ci.append(vd)
        return ''.join(ci)

    def get_valid_ci(self):
        return self.format(vd=str(self.get_validation_digit()))
