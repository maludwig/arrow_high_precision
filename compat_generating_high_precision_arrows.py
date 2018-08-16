#!/usr/bin/env python

import datetime
import time
import arrow
import json

last_arrow = arrow.utcnow()

# Use time.clock on Python < 3.3
high_res_timestamp_function = getattr(time, "perf_counter", time.clock)

def shifted_arrow_method():
    global last_arrow
    this_arrow = arrow.utcnow()
    if this_arrow <= last_arrow:
        this_arrow = last_arrow.shift(microseconds=1)
    last_arrow = this_arrow
    return this_arrow


last_unix_timestamp = time.time()


def adding_microseconds_method():
    global last_unix_timestamp
    last_unix_timestamp = max(time.time(), last_unix_timestamp + 0.000001)
    return arrow.get(last_unix_timestamp)


initial_perf = high_res_timestamp_function()
initial_time = time.time()
perf_time_offset = initial_time - initial_perf


def perf_counter_method():
    global perf_time_offset
    timestamp_in_secs = high_res_timestamp_function() + perf_time_offset
    return arrow.Arrow.utcfromtimestamp(timestamp_in_secs)


def perf_counter_datetime_method():
    global perf_time_offset
    timestamp_in_secs = high_res_timestamp_function() + perf_time_offset
    dt = datetime.datetime.utcfromtimestamp(timestamp_in_secs)
    return arrow.Arrow.fromdatetime(dt)


def sampler(fn, count):
    samples = []
    for i in range(count):
        samples.append(fn())
    different_samples = [samples[0]]
    last = samples[0]
    for i in samples:
        if i != last:
            different_samples.append(i)
            last = i
    return different_samples


def s_sample_summary(samples):
    avg = avg_difference(samples)
    print("{}ms granularity".format(avg * 1000))
    print("{} samples".format(len(samples)))


def dt_sample_summary(samples):
    float_samples = [datetime.datetime.timestamp(x) for x in samples]
    avg = avg_difference(float_samples)
    print("{}ms granularity".format(avg * 1000))
    print("{} samples".format(len(samples)))


def ar_sample_summary(samples):
    float_samples = [x.float_timestamp for x in samples]
    avg = avg_difference(float_samples)
    print("{}ms granularity".format(avg * 1000))
    print("{} samples".format(len(samples)))


def avg_difference(samples):
    last = samples[0]
    total = 0
    for i in samples:
        total += i - last
        last = i
    avg = total / len(samples)
    return avg


def test_everything():
    ITERATIONS = 10010
    TIMESTAMP_FUNCTIONS = [
        # ("s", "time.time", time.time),
        # ("ns", "time.time_ns", time.time_ns),
        # ("ns", "time.perf_counter_ns", time.perf_counter_ns),
        # ("dt", "datetime.datetime.utcnow", datetime.datetime.utcnow),

        ("ar", "arrow.utcnow", arrow.utcnow),
        ("ar", "shifted_arrow_method", shifted_arrow_method),
        ("ar", "adding_microseconds_method", adding_microseconds_method),
        ("ar", "perf_counter_method", perf_counter_method),
        ("ar", "perf_counter_datetime_method", perf_counter_datetime_method),
    ]
    results = []

    for (fn_type, fn_name, fn) in TIMESTAMP_FUNCTIONS:
        print(fn_name + "()")
        start_perf = high_res_timestamp_function()
        samples = sampler(fn, ITERATIONS)
        end_perf = high_res_timestamp_function()
        time_in_ms = (end_perf - start_perf) * 1000
        print("Speed: {} per ms".format(ITERATIONS / time_in_ms))
        if fn_type == "s":
            granularity = avg_difference(samples) * 1000
        elif fn_type == "ns":
            granularity = avg_difference(samples) / 1000000
        elif fn_type == "dt":
            float_samples = [datetime.datetime.timestamp(x) for x in samples]
            granularity = avg_difference(float_samples) * 1000
        elif fn_type == "ar":
            float_samples = [x.float_timestamp for x in samples]
            granularity = avg_difference(float_samples) * 1000
        else:
            raise Exception("What?")
        results.append({
            "name": fn_name,
            "generation_time_in_ms": time_in_ms,
            "generations_per_ms": ITERATIONS / time_in_ms,
            "unique_count": len(samples),
            "granularity_in_ms": granularity,
        })
    results_by_generation_time = sorted(results, key=lambda result: result['generation_time_in_ms'])
    results_by_granularity = sorted(results, key=lambda result: result['granularity_in_ms'])
    print("---       All Results       ---")
    print(json.dumps(results, indent=2))
    print("-------------------------------")
    print("--- Fastest generation time ---")
    print(json.dumps(results_by_generation_time[0], indent=2))
    print("-------------------------------")
    print("---   Highest granularity   ---")
    print(json.dumps(results_by_granularity[0], indent=2))
    print("-------------------------------")


test_everything()
