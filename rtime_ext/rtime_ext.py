from rpython.rlib.rtime import decode_timeval, c_getrusage, RUSAGE_SELF, RUSAGE
from rpython.rtyper.lltypesystem import rffi, lltype


def _make_with_scoped_timer():
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
    return _make_with_scoped_timer()
