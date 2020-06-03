# 接口自动化

## 框架结构讲解：
1.python接口自动化测试框架结构 ( 第一章)——https://blog.csdn.net/weixin_45669374/article/details/105240916
2.python接口自动化测试框架结构 ( 第二章)——https://blog.csdn.net/weixin_45669374/article/details/105247850
3.python接口自动化测试框架结构 ( 第三章)——https://blog.csdn.net/weixin_45669374/article/details/105250939
4.python接口自动化测试框架结构 ( 第四章)——https://blog.csdn.net/weixin_45669374/article/details/105273087
5.python接口自动化测试框架结构 ( 第五章)-数据关联 ——https://blog.csdn.net/weixin_45669374/article/details/105813379


## run testcase 
```shell
# 创建存放log的文件夹
mkdir log
# 启动服务
python sever.py
# 安装依赖
pip install -r requirements.txt
# 运行测试用例
pytest -v run_suite.py -s
```
作者vx:
    dengwoi