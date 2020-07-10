# 说明
平常用到的脚本


# flamesvg.sh
性能分析脚本。根据需要生成火焰图或者以文本的方式统计函数 CPU 占比，主要使用的命令是 perf 命令。

+ 火焰图： 着眼于模块，从函数调用的角度分析 cpu 占比
+ 函数占用文本：  着眼于函数本身，聚合之后的整个函数占用 cpu 的百分比


## help
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

## record
使用 record 命令可以生成 perf.data 文件，抓取 cpu 信息作为原始数据。

使用方式:

```
sh flamesvg.sh record [record_time]
```
注意上面的 record_time 值不应该太大， 不然采集到的 perf.data 数据文件会比较大。一般推荐在 10 一下：

```
sh flamesvg.sh record 10
```

命令结束之后会生成一个 perf.data 文件，这是 cpu 的原始数据文件；

## svg
基于 record 命令生成的 perf.data 进行分析，生成火焰图。

```
sh flamesvg.sh svg
```
命令结束后会生成 perf.svg 火焰图文件；

## txt
基于 record 命令生成的 perf.data 进行分析，生成以文本方式展示的分析结果，着眼点在于 函数聚合之后的 cpu 占比；

```
sh flamesvg.sh txt
```
命令结束后会生成 perf_symbol.data 文件，可以打开查看消耗 cpu 的函数排序；

## all_svg

等于 record 和 svg 两个命令；

```
sh flamesvg.sh all_svg 10
```

## all_txt
等于 record 和 txt 两个命令：

```
sh flamesvg.sh all_txt
```


