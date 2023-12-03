from rpython.rtyper.test.tool import BaseRtypingTest
from rpython.rtyper.lltypesystem import lltype, rffi
from rpython.rlib import rtime

import sys, os, time

from rtime_ext import scoped_getrusage, clock_monotonic


class TestTime(BaseRtypingTest):
    def test_getrusage(self):
        def does_noting():
            time.sleep(0.19)

        def long_loop(n):
            arr = [i for i in range(n)]
            r = 0
            for x in arr:
                r += x
            return r

        N = 10000

        s = rtime.time()
        does_noting()
        e = time.time()

        s_loop = rtime.time()
        long_loop(N)
        e_loop = rtime.time()

        with lltype.scoped_alloc(rtime.RUSAGE) as a:
            rtime.c_getrusage(rtime.RUSAGE_SELF, a)

            does_noting()
            long_loop(N)

            with lltype.scoped_alloc(rtime.RUSAGE) as b:
                rtime.c_getrusage(rtime.RUSAGE_SELF, b)

                a_ru_utime = rtime.decode_timeval(a.c_ru_utime)
                a_ru_stime = rtime.decode_timeval(a.c_ru_stime)
                b_ru_utime = rtime.decode_timeval(b.c_ru_utime)
                b_ru_stime = rtime.decode_timeval(b.c_ru_stime)

                print "time (sleep) %f" % (e - s)
                print "time (loop) %f" % (e_loop - s_loop)
                print "user %f" % (b_ru_utime - a_ru_utime)
                print "system %f" % (b_ru_stime - a_ru_stime)

    def test_scoped_getrusage(self):
        def long_loop(n):
            arr = [i for i in range(n)]
            r = 0
            for x in arr:
                r += x
            return r

        with scoped_getrusage() as t:
            long_loop(10000000)

        print "user ", t.end_utime - t.start_utime
        print "system ", t.end_stime - t.start_stime

    def test_clock_monotonic(self):
        s = clock_monotonic()
        rtime.sleep(0.19)
        e = clock_monotonic()
        assert 0.19 <= e - s
