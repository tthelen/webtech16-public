__author__ = 'Tobias'

_log_level = 3  # from 0=None to 5=extremely verbose


def log(level, msg):
    global _log_level
    if level <= _log_level:
        print("[%d] %s" % (level, msg))
