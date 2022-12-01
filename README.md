# 文档
## 说明
1. 用于 Hawa 相关的所有服务的统一数据计算（避免重复计算）。
## 流程
1. 初始化配置文件
   1. 设置MySQL数据库
   2. 设置Redis数据库
   3. 设置MongoDB数据库
   4. 设置 COMPLETED True
2. 启动服务
   1. 启动MongoDB数据库
   `` .connect()``