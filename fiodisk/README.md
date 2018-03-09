# 说明
使用 fio 工具测试 SSD 以及 SATA 磁盘的性能，绘制 BS/IOPS、BS/BW 之间的性能曲线。

# FIO 使用指南
见这篇博客[fio 使用指南](http://blog.itzhoulin.com/2015/12/24/fio-man-guide/#IO%E5%BC%95%E6%93%8E)


# FIO 配置文件
详细请查看 fio 配置脚本[bs.conf](https://github.com/smaugx/dailydemo/blob/master/fiodisk/test/ssd/bs.conf)

关键参数:

+ ioengine=libaio : 使用异步 IO 引擎
+ direct=1 : true,则标明采用non-buffered io
+ iodepth=16 : 用来提高并发度，保证 IO 队列深度为一个我们想要的值
+ numjobs=20 : 创建特定数目的job副本，可能是创建大量的线程/进程来执行同一件事

# 测试方法
具体使用的时候只需要更改如下两个参数:

+ rw=randrw
+ filename=/dev/sda

```
$ fio bs.conf > randrw.log
```

更改 rw 参数为(rw、read、write、randrw、randread、randwrite) 可以分别测试不同的读写模式，收集数据

更改 filename 参数为 SSD 或者 SATA 对应的盘符


# 数据清洗，整理
收集得到如下的一些文件:

```
randread.log  randrw.log  randwrite.log  read.log  rw.log  write.log
```

然后执行脚本:

```
$ sh do.sh
```
清理后的数据保存在文件名为 ret3 的文件中。


# 性能曲线
使用 highcharts 进行数据可视化。
