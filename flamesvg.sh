#!/usr/bin/env bash
echo_and_run() { echo "$*" ; "$@" ; }

params_num=$#



osinfo=`awk -F= '/^NAME/{print $2}' /etc/os-release |awk -F ' ' '{print $1}' |awk -F '\"' '{print $2}'`

ubuntu_os="Ubuntu"
centos_os="CentOS"
osname_linux="Linux"
osname_darwin="Darwin"


if [  $# -lt 1 ]; then
    echo "error param"
    echo "Usage: ./flamesvg.sh [command]"
    echo ""
    echo "     record       using 'perf record' to generate perf.data"
    echo "     svg          after using [record] command, than using [svg] to generate flamegraph perf.svg"
    echo "     txt          after using [record] command, than using [txt] to generate cpu-percentage of symbol(function) perf_symbol.data"
    echo "     all_svg      equal to [record] + [svg] command"
    echo "     all_txt      equal to [record] + [txt] command"
    exit -1
fi

if [ ! -d "FlameGraph" ]; then
    if [ $osinfo = ${ubuntu_os} ]
    then
        echo "Ubuntu"
	echo_and_run echo "sudo apt install  linux-tools-common -y" | bash -
	echo_and_run echo "sudo apt install git  -y" | bash -
        echo_and_run echo "git clone https://github.com/brendangregg/FlameGraph" |bash -
    elif [ $osinfo = ${centos_os} ]
    then
        echo "Centos"
        echo_and_run echo "sudo yum install perf -y" |bash -
        echo_and_run echo "sudo yum install git -y"  |bash -
        echo_and_run echo "git clone https://github.com/brendangregg/FlameGraph" |bash -
    else
        echo "unknow osinfo:$osinfo"
	exit -1
    fi
fi

if [  $1 = 'record' ]; then
    record_time=10
    if [  $2 ]; then
        record_time=$2
        echo "perf record time is ${record_time}"
    fi

    rm -rf perf.*
    echo_and_run echo "sudo perf record --call-graph dwarf -a sleep ${record_time}" |bash -
    exit 0
fi

if [  $1 = 'svg' ]; then
    echo_and_run echo "sudo perf script -i perf.data > perf.unfold" |bash -
    echo_and_run echo "./FlameGraph/stackcollapse-perf.pl perf.unfold > perf.folded" |bash -
    echo_and_run echo "./FlameGraph/flamegraph.pl perf.folded > perf.svg" |bash -

    echo "flame svg file generated: perf.svg"
    echo_and_run echo "ls perf.svg" |bash -
    exit 0
fi

if [  $1 = 'txt' ]; then
    echo_and_run echo "sudo perf report -i perf.data --no-children --sort comm,symbol > perf_symbol.data" |bash -

    echo "perf_symbol(function).data generated"
    echo_and_run echo "ls perf_symbol.data" |bash -
    exit 0
fi


if [  $1 = 'all_svg' ]; then
    record_time=10
    if [  $2 ]; then
        record_time=$2
        echo "perf record time is ${record_time}"
    fi

    rm -rf perf.*
    echo_and_run echo "sudo perf record --call-graph dwarf -a sleep ${record_time}" |bash -

    echo_and_run echo "sudo perf script -i perf.data > perf.unfold" |bash -
    echo_and_run echo "./FlameGraph/stackcollapse-perf.pl perf.unfold > perf.folded" |bash -
    echo_and_run echo "./FlameGraph/flamegraph.pl perf.folded > perf.svg" |bash -

    echo "flame svg file generated: perf.svg"
    echo_and_run echo "ls perf.svg" |bash -
    exit 0
fi

if [  $1 = 'all_txt' ]; then
    record_time=10
    if [  $2 ]; then
        record_time=$2
        echo "perf record time is ${record_time}"
    fi

    rm -rf perf.*
    echo_and_run echo "sudo perf record --call-graph dwarf -a sleep ${record_time}" |bash -
    echo_and_run echo "ls -al perf.data" |bash -
    echo_and_run echo "sudo perf report -i perf.data --no-children --sort comm,symbol > perf_symbol.data" |bash -

    echo "perf_symbol(function).data generated"
    echo_and_run echo "ls perf_symbol.data" |bash -
    exit 0
fi


echo "error param"
echo "Usage: ./flamesvg.sh [command]"
echo ""
echo "     record       using 'perf record' to generate perf.data"
echo "     svg          after using [record] command, than using [svg] to generate flamegraph perf.svg"
echo "     txt          after using [record] command, than using [txt] to generate cpu-percentage of symbol(function) perf_symbol.data"
echo "     all_svg      equal to [record] + [svg] command"
echo "     all_txt      equal to [record] + [txt] command"
