Title: Hive整体优化策略
Date: 2014-12-03 00:20
Modified: 2014-12-03 00:20
Category: bigdata
Tags: hive
Slug: hive-optimization
Author: jacksu
ummary:hive可以从几个方面进行优化，从系统角度看：整体架构、MR阶段、JOB以及平台都可以进行优化。从用户角度看:了解SQL执行过程以及业务数据特点，调整SQL语句进行优化。

#一 整体架构优化
现在hive的整体框架如下，计算引擎不仅仅支持Map/Reduce，并且还支持Tez、Spark等。根据不同的计算引擎又可以使用不同的资源调度和存储系统。

![hive_frame](.http://jacksu.github.io/static/bigdata/hive_frame)

整体架构优化点：
1 根据不同业务需求进行日期分区，并执行类型动态分区。
相关参数设置：
0.14中默认hive.exec.dynamic.partition=ture
2 为了减少磁盘存储空间以及I/O次数，对数据进行压缩
相关参数设置：
job输出文件按照BLOCK以Gzip方式进行压缩。
mapreduce.output.fileoutputformat.compress=true
mapreduce.output.fileoutputformat.compress.type=BLOCK
mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.GzipCodec
map输出结果也以Gzip进行压缩。
mapreduce.map.output.compress=true
mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.GzipCodec
对hive输出结果和中间结果进行压缩。
hive.exec.compress.output=true
hive.exec.compress.intermediate=true
3 hive中间表以SequenceFile保存，可以节约序列化和反序列化的时间
相关参数设置：
hive.query.result.fileformat=SequenceFile
4 yarn优化，在此不再展开，后面专门介绍。
#二 MR阶段优化
hive操作符有：

![hive_oper](.http://jacksu.github.io/static/bigdata/hive_oper)

执行流程为：

![hive_oper_flow](.http://jacksu.github.io/static/bigdata/hive_oper_flow)

reduce切割算法：
相关参数设置，默认为：
hive.exec.reducers.max=999
hive.exec.reducers.bytes.per.reducer=1G 
reduce task num=min{reducers.max,input.size/bytes.per.reducer}，可以根据实际需求来调整reduce的个数。
#三 JOB优化
##1 本地执行
默认关闭了本地执行模式，小数据可以使用本地执行模式，加快执行速度。
相关参数设置：
hive.exec.mode.local.auto=true 
默认本地执行的条件是，hive.exec.mode.local.auto.inputbytes.max=128MB， hive.exec.mode.local.auto.tasks.max=4，reduce task最多1个。
性能测试：


|数据量（万）|操作|正常执行时间（秒)|本地执行时间（秒）|
|:---:|:---:|:---:|:---:|
|170|group by|36|16|
|80|count|34|6|

##2 mapjoin
默认mapjoin是打开的，
hive.auto.convert.join.noconditionaltask.size=10MB


装载到内存的表必须是通过scan的表（不包括group by等操作），如果join的两个表都满足上面的条件，/\*mapjoin\*/指定表格不起作用，只会装载小表到内存，否则就会选那个满足条件的scan表。

#四 SQL优化
整体的优化策略如下：

1. 去除查询中不需要的column
2. Where条件判断等在TableScan阶段就进行过滤
3. 利用Partition信息，只读取符合条件的Partition
4. Map端join，以大表作驱动，小表载入所有mapper内存中
5. 调整Join顺序，确保以大表作为驱动表
6. 对于数据分布不均衡的表Group by时，为避免数据集中到少数的reducer上，分成两个map-reduce阶段。第一个阶段先用Distinct列进行shuffle，然后在reduce端部分聚合，减小数据规模，第二个map-reduce阶段再按group-by列聚合。
7. 在map端用hash进行部分聚合，减小reduce端数据处理规模。
#五 平台优化
1hive on tez

![hive_on_tez](.http://jacksu.github.io/static/bigdata/hive_on_tez)

2 spark SQL大趋势

![spark_sql](.http://jacksu.github.io/static/bigdata/spark_sql)

#总结
上面主要介绍一些优化思想，有些优化点没有详细展开，后面分别介绍yarn的优化细节、SQL详细的优化实例以及我们在Tez、spark等框架优化结果。最后用一句话共勉：边coding，边优化，优化无止境。
