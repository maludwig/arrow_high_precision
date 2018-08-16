#!/usr/bin/env python
from __future__ import print_function

import time

if getattr(time, "perf_cozzzunter", None):
    print("It has time.perf_cozzzunter")

if getattr(time, "perf_counter", time.clock):
    print("It has time.perf_counter")
    print(time.perf_counter())
    time.sleep(1)
    print(time.perf_counter())

if time.clock:
    print("It has time.clock")
    print(time.clock())
    time.sleep(1)
    print(time.clock())
