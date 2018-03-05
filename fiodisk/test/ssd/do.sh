#!/bin/sh

# 更改 rwmode 可以测试不同读写模式下的磁盘性能,标准输出重定向到*rwmode*.log 里
# 比如: fio bs.conf > randrw.log

#此脚本实现功能：分析处理*.log，最终得到清洗后的数据



#the first time filter
for i in `ls *.log`; do echo ' '; echo [$i]; grep -E 'groupid|iops|bw=' $i; done  > ret1

#the second time filter
cat ret1  |cut -d ':' -d ','  -f 1,2,3 > ret2

#the third time filter
rm -f ret3
cat ret2 | while read line; do
  newline="$line";
  first=`echo $newline |cut -d '-' -f 1`;
  if [ "$first" = "fio" ];then
    newline=`echo $newline |cut -d ':' -f 1`;
    newline="$newline:"
  fi
  echo $newline >> ret3;
done
