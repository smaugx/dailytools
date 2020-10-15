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


# iftop_remote_ip.py
调用 iftop 命令从 remote_ip 维度统计发送接收流量，脚本中限定了只统计本地 80 和 443 端口，实际场景下可以修改成其他过滤条件或者去掉。

```
remote_ip:124.160.217.1 send:1450 Kb/s recv:7 Kb/s
remote_ip:124.160.217.1 send:3160 Kb/s recv:20 Kb/s
remote_ip:124.160.217.1 send:2407 Kb/s recv:26 Kb/s
remote_ip:124.160.217.1 send:2696 Kb/s recv:25 Kb/s
remote_ip:124.160.217.2 send:2729 Kb/s recv:25 Kb/s
remote_ip:124.160.217.3 send:2852 Kb/s recv:26 Kb/s
remote_ip:124.160.217.4 send:2650 Kb/s recv:23 Kb/s
remote_ip:124.160.217.1 send:2539 Kb/s recv:25 Kb/s
remote_ip:124.160.217.3 send:2362 Kb/s recv:24 Kb/s
remote_ip:124.160.217.2 send:2741 Kb/s recv:24 Kb/s
remote_ip:124.160.217.4 send:2667 Kb/s recv:23 Kb/s
remote_ip:124.160.217.2 send:2679 Kb/s recv:21 Kb/s
remote_ip:124.160.217.1 send:2540 Kb/s recv:28 Kb/s
```


# mykill
简单封装了下 kill 命令，本质上是 killall 命令的实现，只不过更加友好一点。

```
smaug@smaug-VirtualBox:~$ mykill  -h
error param
grep all program name  and kill all
Usage: mykill [program_name] [yes/no]
```

# filscan.py
爬取 https://filscan.io/#/tipset/address-detail?address=f02301 网站的数据

```
From,Receipt,MessageID,Value,Height,To,Time,Method
f3qhvpg5byv25lcdch2z62ml7jp3rxnpt5ogg5jtokjwv7q6sqwzd2e4qw2sqh5kvh7nitnejhao6bc5xnqdna,OK,bafy2bzacedwhwgnhzjsgljm5shbiq5ni7je562ho7uus6fjno4gjgzitsek6a,0.0351423918839 FIL,147292,f02301,2020-10-15 09:26:00,ProveCommitSector
f3tckh5m4xq6rttaosbzh2xjk4wbwzzxjft4srbqup64tmywhofhfug55yuvybhtw7mjcxzztwook2xkuzkggq,OK,bafy2bzaceb5vuuafr4kxslnym5bymjujdh5ophpr6mxqlazldhyva75bgpine,0.0 FIL,147289,f02301,2020-10-15 09:24:30,DeclareFaultsRecovered
f3qhvpg5byv25lcdch2z62ml7jp3rxnpt5ogg5jtokjwv7q6sqwzd2e4qw2sqh5kvh7nitnejhao6bc5xnqdna,OK,bafy2bzacedxubn3patupbnvwiaon7nq6d7psiv2rgeqamm2roxd5kwg7i7gtk,0.0351766999492 FIL,147289,f02301,2020-10-15 09:24:30,ProveCommitSector
f3qhvpg5byv25lcdch2z62ml7jp3rxnpt5ogg5jtokjwv7q6sqwzd2e4qw2sqh5kvh7nitnejhao6bc5xnqdna,OK,bafy2bzacebmhkr6h5utipjqtf6bt2bbuer2l7z4ky7onlpma2cr22giyk565a,0.0351584198055 FIL,147289,f02301,2020-10-15 09:24:30,ProveCommitSector
f3qhvpg5byv25lcdch2z62ml7jp3rxnpt5ogg5jtokjwv7q6sqwzd2e4qw2sqh5kvh7nitnejhao6bc5xnqdna,OK,bafy2bzaceasyr2bt3tynwufadzxvhryybly4vfwa4psjw7j6rg66o2l66fedy,0.168976637674 FIL,147288,f02301,2020-10-15 09:24:00,PreCommitSector
f3qhvpg5byv25lcdch2z62ml7jp3rxnpt5ogg5jtokjwv7q6sqwzd2e4qw2sqh5kvh7nitnejhao6bc5xnqdna,OK,bafy2bzacedceqm2isw7rsuiroe4sninkql4msibjn4jt2spnyjelcoft7qc7s,0.168990631288 FIL,147287,f02301,2020-10-15 09:23:30,PreCommitSector
f3qhvpg5byv25lcdch2z62ml7jp3rxnpt5ogg5jtokjwv7q6sqwzd2e4qw2sqh5kvh7nitnejhao6bc5xnqdna,OK,bafy2bzaceboueg6uvwhi7nthrtlrs7hc6doiycurhqbywzktmmoera4uqgfis,0.0352552658287 FIL,147286,f02301,2020-10-15 09:23:00,ProveCommitSector
f3qhvpg5byv25lcdch2z62ml7jp3rxnpt5ogg5jtokjwv7q6sqwzd2e4qw2sqh5kvh7nitnejhao6bc5xnqdna,OK,bafy2bzacectjyk77l3t5tuoxkotjzo33sobp6mrdtbwousfl7tj5scj2rtp32,0.169004548953 FIL,147286,f02301,2020-10-15 09:23:00,PreCommitSector
f3qhvpg5byv25lcdch2z62ml7jp3rxnpt5ogg5jtokjwv7q6sqwzd2e4qw2sqh5kvh7nitnejhao6bc5xnqdna,OK,bafy2bzacecb7okvcovy42hqxr5jyfw2dlnftom4zan6tvasmer2efvnzoq774,0.0352578666153 FIL,147284,f02301,2020-10-15 09:22:00,ProveCommitSector
```
