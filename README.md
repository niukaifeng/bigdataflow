——待办任务——
1. 业务流程比较难看   （完成）
2. 三方会签注意控件     （完成）
3. 文件上传只保存了一个，项目名称顺序（完成）
4. “标题”改成“项目名称”前端js处理，施工进度横条可视化  
5. 结束项目的“工单详情”信息展示（展现表单），可下载所有文件  （完成）

6. 所有工单只能管理员、专家看，其他人只能待办、相关，创建工单只能企业和管理员

7. 上一步工单详情，弄成按照流程的报表形式
8. 自动生成建议项目编号110/N00+年份+编号，并且建议项目编号可更改（根据需求再定）
9. 左上角的搜索功能
10. 日期时间和附件的背景颜色
11. 网站发布问题
12. 发邮件问题
13. 修改admin页面：用户添加电话信息，用户分组分角色管理
14. 调用bootstrap或echart与bower和Adminlte的页面显示关系
15. 发短信
16. lonnflow可视化，和自定义的可视化展示
——以下已完成——
1. 参考workflow和shutongflow，是否要建立bigdataflow
2. 写一个页面，连接上接口
3. 完成一个110工法页面显示，调用loonflow里的任意一张表
4. 梳理bigdataflow项目的思维导图
5. 继续研究loonflow的接口调用，接口获取数据在bigdataflow中的使用方法
6. 验证详情页面控件填写的数据，能否传到数据库，结果传不到数据库
7. 弄清楚suggestion字段是怎么传到后台数据库的，自定义字段怎么按照suggestion方式上传数据库
8. 学习html的控件标签，补齐详情页面的其他的几个控件
9. 文件上传控件与文件上传下载的的实现
10. 驳回功能
11. 文件保存多级目录
12. 第二步审核时看到第一步填写的内容（完成)
13. 文件下载，鼠标提示的链接（完成）
14. 驳回时，可以不填写必填控件 (完成)
15. 一个split()bug       （完成）

固定且不能改变的字段
b_guanliyuanshenpi_char_xiangmubianhao

g_sanfanghuiqian_text_sanfanghuiqian

> 新增

FLOWINPUTSTR
   * 总恒阻锚索/米               j_shigongjindu_float_zonghengzumaosuo
   * 当前已完成恒阻锚索/米        j_shigongjindu_float_muqianhengzumaosuo
   * 总切缝钻孔/米               j_shigongjindu_float_zongqiefengzhuankong
   * 当前已完成切缝钻孔/米        j_shigongjindu_float_muqianqiefengzhuankong
   * 总爆破裂缝/米               j_shigongjindu_float_zongbaopoliefeng
   * 当前已完成爆破裂缝/米        j_shigongjindu_float_muqianbaopoliefeng


## 关于数据保存工单信息的想法

> 进入 施工进度
* 查看 -- 数据库查询数据
* 保存 -- 数据库插入数据

## TODO 顾
[] 整合固定字段
[] 单独显示进度条
[] 数据柏村    


