
## 信息
### 配置
#### ssh连接
7-1  
IP:10.0.0.170  

7-2
IP：10.0.0.123  
password：123   
[VScode配ssh--bilibili教程前三分钟](https://www.bilibili.com/video/BV1Ld4y1M7EV/?share_source=copy_web&vd_source=b987eb909065c989d772c8c7a783e243)
#### tightVNC
Remote Host：10.0.0.123:5901  
password：az888888  
#### 狗
7-1 & 7-2  
名字:az
### 提醒
+ 同时写代码时注意保存
+ build之前要先在终端输入`cd workplace`,否则无法更新所做的修改!
### 参考资料
#### 二代机器狗的开源信息：
1. [文档博客](https://miroboticslab.github.io/blogs/#/)
2. [源码地址](https://github.com/MiRoboticsLab/cyberdog_ws)

#### ROS学习参考
1. [发布订阅节点](https://blog.csdn.net/qq_38649880/article/details/104423203)
2. 
#### 其它资料
1. [第二次培训的PPT和录屏](https://cloud.tsinghua.edu.cn/d/9aefef66ac9542a6944d/)
2. [代码托管](https://git.tsinghua.edu.cn/cyberdog_competition/2024)
3. [whf的github仓库](https://github.com/HeFeiW/cyberdog_az)
## 进度
#### todo：
+ walk中添加“更新”方法，订阅话题更新dist成员，
在basic_node中创建suber实例，实时调用更新函数更新dist并返回到控制台。
+ 主函数basic_move,订阅超声，根据距离决定直走/转弯，调用相应的指令。
### 进度记录
#### 04.23 李想 何冠奇 王鹤霏
+ 主要是尝试理解了一下ros2的工作机制: subscribe & publish / server & client
+ 修改了walk.py,实现在执行小步慢走的同时向终端返回distance,但没有实现实时更新distance
+ 帮大家踩了一个大坑(bushi)


### 常用命令行
1. 打开相机： 
    + ros2 launch realsense2_camera on_dog.py
    + ros2 lifecycle set /camera/camera configure
    + ros2 lifecycle set /camera/camera activate
2. 运行
    + cd workplace
    + colcon build
    + ros2 run learning XXX