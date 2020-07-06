#!/usr/bin/env bash
echo_and_run() { echo "$*" ; "$@" ; }

if [ ! -d "FlameGraph" ]; then
    echo_and_run echo "sudo yum install perf -y" |bash -
    echo_and_run echo "sudo yum install perf -y" |bash -
    echo_and_run echo "sudo yum install git -y"  |bash -
    echo_and_run echo "git clone https://github.com/brendangregg/FlameGraph" |bash -
fi

record_time=10
if [  $1 ]; then
    record_time=$1
    echo "perf record time is ${record_time}"
fi

rm -rf perf.*
echo_and_run echo "sudo perf record --call-graph dwarf -a sleep ${record_time}" |bash -
echo_and_run echo "sudo perf script -i perf.data > perf.unfold" |bash -
echo_and_run echo "./FlameGraph/stackcollapse-perf.pl perf.unfold > perf.folded" |bash -
echo_and_run echo "./FlameGraph/flamegraph.pl perf.folded > perf.svg" |bash -

echo "flame svg file generated: perf.svg"
echo_and_run echo "ls perf.svg" |bash -
