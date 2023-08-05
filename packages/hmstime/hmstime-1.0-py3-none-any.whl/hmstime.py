import re
from datetime import timedelta

xpr = re.compile(r"""
    (?:(?P<hours>[0-9]+(?=h)))?h?
    (?:(?P<minutes>[0-9]+(?=m)))?m?
    (?:(?P<seconds>[0-9]+(?=s)))?s?
""", re.VERBOSE)

def parse(timestr):
   s = timestr.replace(' ', '')
   return re.match(xpr, s).groupdict()

def todelta(timestr):
   parsed = parse(timestr)
   return timedelta(**{k: int(v) for k, v in parsed.items() if v})

def toseconds(timestr):
   return int(todelta(timestr).total_seconds())

