"""
Unit test for amortization_grid.py
"""

import os
import amortization_grid as ag


class Test_AG:

    p = 25000.00  # principle
    r = 4.5/100  # interest rate
    m = 36  # number of payments
    c = 743.67  # test check value

    def test_i_amortize(self):
        d = ag.i_amortize(self.p, self.r, self.m)
        assert self.c == round(d, 2)

    def test_i_schedule(self):
        d = ag.i_schedule(self.p, self.r, self.m)
        assert 36 == len(d)
        assert self.c == d[35]['balance']

    def test_o_schedule(self):
        r = ag.i_schedule(self.p, self.r, self.m)
        d = ag.o_schedule(r)
        assert self.c == float(d['balance'][35][1:].replace(',', ''))

    def test_xlwriter(self):
        r = ag.i_schedule(self.p, self.r, self.m)
        d = ag.xlwriter(r, self.p, self.r, self.m, 'output')
        assert 0 == d[0]
        os.system('rm output.xlsx')
