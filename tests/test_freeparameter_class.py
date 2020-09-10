from .context import pset
from nose.tools import raises

import numpy as np


class TestFreeParameter:

    @classmethod
    def setup_class(cls):
        cls.p0 = pset.FreeParameter('var0__FREE', 'normal_var', 0, 1)
        cls.p1 = pset.FreeParameter('var1__FREE', 'lognormal_var', 1, 2)
        cls.p2 = pset.FreeParameter('var2__FREE', 'loguniform_var', 0.01, 100)
        cls.p3 = pset.FreeParameter('var2__FREE', 'uniform_var', 0, 10)
        cls.p4 = pset.FreeParameter('var2__FREE', 'uniform_var', 0, 10, bounded=False)

    @classmethod
    def teardown_class(cls):
        pass

    def test_check_init(self):
        print(self.p0.value)
        assert self.p0.value is None
        assert self.p0.type == 'normal_var'
        assert not self.p0.bounded

        assert not self.p1.bounded
        assert self.p1.lower_bound == 0.0
        assert np.isinf(self.p1.upper_bound)

        assert self.p2.upper_bound == 100

        assert self.p3.bounded
        print(self.p4.bounded)
        assert not self.p4.bounded

    @raises(pset.OutOfBoundsException)
    def test_check_erroneous_assignment(self):
        pset.FreeParameter('var2__FREE', 'loguniform_var', 0.01, 100, value=1000)

    def test_distribution(self):
        xs = [self.p3.sample_value().value for x in range(100000)]
        for x in xs:
            assert self.p3.lower_bound <= x < self.p3.upper_bound
        ys = [self.p0.sample_value().value for x in range(100000)]
        assert np.all(np.array(ys)>=0.0)

    def test_sample_value(self):
        p0s = self.p0.sample_value()
        assert p0s.value is not None

    def test_freeparameter_equality(self):
        p6 = self.p0.sample_value()
        p0s = self.p0.set_value(p6.value)
        print(p0s, p6)
        assert p6 == p0s

    def test_add(self):
        p7 = self.p0.set_value(1)
        p7a = p7.add(1)
        assert p7a.value == 2
        p8 = self.p2.set_value(1)
        p8a = p8.add(1)
        assert p8a.value == 10

    def test_diff(self):
        p9 = self.p0.set_value(1)
        p10 = self.p0.set_value(2)
        assert p9.diff(p10) == -1

        p11 = self.p2.set_value(10)
        p12 = self.p2.set_value(100)
        assert p12.diff(p11) == 1

    def test_reflect(self):
        assert self.p3.set_value(11).value == 9
        assert self.p3.set_value(12).value == 8
        assert self.p3.set_value(25).value == 5
        assert self.p2.set_value(1000).value == 10

    def test_set_value(self):
        p13 = self.p0.set_value(1)
        assert p13.lower_bound == self.p0.lower_bound
        assert p13.upper_bound == self.p0.upper_bound
        p14 = self.p4.set_value(100)
        assert p14.lower_bound == self.p4.lower_bound
        assert p14.upper_bound == self.p4.upper_bound

    @raises(pset.OutOfBoundsException)
    def test_no_reflect(self):
        self.p3.set_value(11, False)
