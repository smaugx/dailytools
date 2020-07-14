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


# nat_birth_attach.py
生日攻击算法的实现和验证，为 p2p 打洞（对称性）提供理论基础（端口预测）。

```
p: 0.507297 > rate:0.5 k: 23 success
when total_samples is 365, if request for rate greater than 0.5, then try at least 23 times is ok

p: 0.500722 > rate:0.5 k: 302 success
when total_samples is 65536, if request for rate greater than 0.5, then try at least 302 times is ok

p: 0.701186 > rate:0.7 k: 398 success
when total_samples is 65536, if request for rate greater than 0.7, then try at least 398 times is ok

p: 0.801039 > rate:0.8 k: 460 success
when total_samples is 65536, if request for rate greater than 0.8, then try at least 460 times is ok

p: 0.900755 > rate:0.9 k: 550 success
when total_samples is 65536, if request for rate greater than 0.9, then try at least 550 times is ok

p: 0.990025 > rate:0.99 k: 770 success
when total_samples is 64512, if request for rate greater than 0.99, then try at least 770 times is ok
```


打开文件直接修改 total_samples 和 rate 值就可以验证在总样本量为  total_samples 的场景下，当需要满足至少两个样本一样的概率大于等于rate值需要的尝试次数
。
