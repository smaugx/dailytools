# 说明
平常用到的脚本


# flamesvg.sh
性能分析脚本。根据需要生成火焰图或者以文本的方式统计函数 CPU 占比，主要使用的命令是 perf 命令。


 ```
 [root@localhost smaug]# sh flamesvg.sh 
error param
Usage: ./flamesvg.sh [command]

     record       using 'perf record' to generate perf.data
     svg          after using [record] command, than using [svg] to generate flamegraph perf.svg
     txt          after using [record] command, than using [txt] to generate cpu-percentage of symbol(function) perf_symbol.data
     all_svg      equal to [record] + [svg] command
     all_txt      equal to [record] + [txt] command
  
 ```
 
 使用 record 命令可以生成 perf.data 文件
