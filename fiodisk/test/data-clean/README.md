# 功能说明
清洗原始数据，整理得最终所需数据

# 数据文件说明
+ ssd_data.source/sata_data.source : 原始数据
+ ssd_data.json/sata_data.json : 清洗为 json 格式的数据
+ result : 前端 highcharts 所需最终数据


# py 脚本说明
+ source_data_to_json.py : 清洗数据为 json 格式
+ redisdump.py : 数据存储到 redis 永久保存
+ getdata.py : 根据前端所需格式，查询 redis 然后构造格式化数据，实际情况直接读取结果文件 result 返回
