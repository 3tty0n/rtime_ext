from rpython.rlib.rtime import (
    decode_timeval,
    external,
    c_getrusage,
    c_clock_gettime,
    CConfigForClockGetTime,
    RUSAGE_SELF,
    RUSAGE,
    HAS_CLOCK_GETTIME,
    CLOCK_MONOTONIC,
    TIMESPEC,
)
from rpython.rtyper.lltypesystem import rffi, lltype

if HAS_CLOCK_GETTIME:
    eciclock = CConfigForClockGetTime._compilation_info_
    c_clock_gettime_monotonic = external('clock_gettime',
                                         [lltype.Signed, lltype.Ptr(TIMESPEC)],
                                         rffi.INT, releasegil=False,
                                         save_err=rffi.RFFI_SAVE_ERRNO,
                                         compilation_info=eciclock)


def _make_with_scoped_getrusage():
    class ScopedTimer:
        def __init__(self):
            # TODO: improve accuracy
            self.start_utime = None
            self.start_stime = None
            self.end_utime = None
            self.end_stime = None

        def __enter__(self):
            with lltype.scoped_alloc(RUSAGE) as a:
                c_getrusage(RUSAGE_SELF, a)
                self.start_utime = decode_timeval(a.c_ru_utime)
                self.start_stime = decode_timeval(a.c_ru_stime)
            return self

        def __exit__(self, type, value, traceback):
            with lltype.scoped_alloc(RUSAGE) as a:
                c_getrusage(RUSAGE_SELF, a)
                self.end_utime = decode_timeval(a.c_ru_utime)
                self.end_stime = decode_timeval(a.c_ru_stime)

    return ScopedTimer()


def scoped_getrusage():
    return _make_with_scoped_getrusage()


def clock_monotonic():
    if HAS_CLOCK_GETTIME:
        with lltype.scoped_alloc(TIMESPEC) as a:
            if c_clock_gettime_monotonic(CLOCK_MONOTONIC, a) == 0:
                return (
                    float(rffi.getintfield(a, "c_tv_sec"))
                    + float(rffi.getintfield(a, "c_tv_nsec")) * 0.000000001
                )
    with lltype.scoped_alloc(RUSAGE) as a:
        c_getrusage(RUSAGE_SELF, a)
        result = decode_timeval(a.c_ru_utime) + decode_timeval(a.c_ru_stime)
    return result
