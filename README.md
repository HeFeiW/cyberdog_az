
## 信息
### 配置
#### 狗
+ 7-1  
    IP:10.0.0.170  
    password：123
    namespace：az1
+ 7-2
    IP：10.0.0.123  
    password：123   
    namespace：az  
    tightVNC：  
        Remote Host：10.0.0.123:5901  
        password：az888888 
[VScode配ssh--bilibili教程前三分钟](https://www.bilibili.com/video/BV1Ld4y1M7EV/?share_source=copy_web&vd_source=b987eb909065c989d772c8c7a783e243)

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
+ 四段式  
    - 上位机：球门坐标，球坐标，前锋坐标，计算延长线，最短路线走至距球一定距离
    - 摄像头：原地角度旋转，检测x坐标位于画面中央（x==320）
    - 摄像头/深度相机：后退一定距离
    - 摄像头/深度相机：快走【一定时间】踢球
+ socket  
    - 
+ bash
### 进度记录
#### 04.23 李想 何冠奇 王鹤霏
+ 主要是尝试理解了一下ros2的工作机制: subscribe & publish / server & client
+ 修改了walk.py,实现在执行小步慢走的同时向终端返回distance,但没有实现实时更新distance
+ 帮大家踩了一个大坑(bushi)
#### 05.02 李想 王鹤霏
+ 进度：无 精神状态：凉好
+ 尝试source bash失败（每次启动terminal重新执行activate，耗时长，且启动过一次后在尝试启动会transitioning failed）；输入命令行后rgb相机打不开，topic echo无返回值。
#### 05.03 李想
+ 解决了莫名其妙进入虚拟环境的问题（卸载VScode python插件）
+ 解决了（至少在一次调试里成功了。。）rgb相机打不开，/image_rgb主题echo不回来数据的问题
+ 实现了rgb相机publish出去的/image_rgb话题的订阅，并且成功在电脑上可视化。（需要在电脑上下载Xming软件并配置，需要在狗的.bashrc文件里配置）
+ 成功一次后，重启后仍然存在相机打不开的问题，不知道哪里出现了问题。。。
+ 抱了自01 胡振桦学长的大腿 感谢他
#### 05.04 李想 王鹤霏 （以及背后的学长和copilot）
+ 成功开启rgb相机
+ 配好Xming在电脑上实时显示rgb相机图形画面
+ cv2识别画面中目标颜色并计算圆球的x、y坐标和像素面积
+ socket接收上位机回传的坐标信息
+ 规划了一下射门策略，目前计划用快走撞球
### 常用命令行
1. 打开相机： （废弃）
    + ros2 launch realsense2_camera on_dog.py
    + ros2 lifecycle set /camera/camera configure
    + ros2 lifecycle set /camera/camera activate
2. 运行
    + cd workplace
    + colcon build
    + ros2 run learning XXX
3. 启动rgb相机
    + 窗口1:ros2 launch camera_test stereo_camera.py
    + 窗口2:# 启动lifecycle的接口
    + ros2 lifecycle set /az/camera/camera configure 
    + ros2 lifecycle set /az/camera/camera activate 
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}" 
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"
4. 连接Xming
    + export DISPLAY=10.0.0.184:0.0
    + xhost +
### 运动参数
飞扑距离
x==410,y==378,area==31450
上位机：
摄像头坐标系，左-右+，球门y坐标7.9 x坐标0.1
绿球在摄像头中心位置：只用x坐标定位：260-400

#### 如何配置Xming实现远程主机（Windows）屏显
##### 远程主机（自己的电脑，此处用的是Windows）
+ 下载Xming[下载网址](https://sourceforge.net/projects/xming/?source=typ_redirect)
+ 打开Xming安装目录，目录下x0.hosts文件，在localhost下另起一行粘贴入{本机IP}（10.0.0.123/168），保存
+ 如果在上一步之前打开过Xming，要关闭后重启
+ 远程配置完毕
+ 查看【远程IP】：WindowsPowershell输入ipconfig查看局域网IPv4 ip地址（10.0.0.xxx）
+ 
##### 本机（此处为狗子的linux系统）  
+ sudo apt-get install x11-xserver-utils
+ xstart（只需执行一次，之后重启狗子无需再执行，下面其余命令在重启后要重新执行）
+ export DISPLAY={远程IP}:0.0
+ xhost +
\* 切换rgb相机传回图像类别：/opt/ros2/cyberdog/share/camera_test/config（注意**不在**/home/mi目录下，要在open folder那边直接复制上面路径）下yaml文件，修改format_rgb参数（改为rgb对应选项）



#### 05.05上午  周子睿 李想
+   如何将大象放入冰箱
    + 让狗转，直到球处于视野中心（实现方法：让绿球x坐标位于260-400间）
    + 维护一条球门到球的直线，计算出狗在这条直线的左还是右
    + 让狗平移到直线上
    + 让狗转，直到球处于视野中心
    + 快走撞球
+上午进度：熟悉了所有进度，实现了接收上位机坐标并存储为坐标形式，实现了维护一条直线，编写了旋转直到中心代码，还未调试成功。
+to do list:计算在直线左还是右，实现平移到直线上，实现快走撞球。编写守门狗。

#### 05.05 晚  whf lx wmy lhy hgq

+   进度：
     + 基本实现了所有小模块！！欢呼~~O(∩_∩)O~~
     + 小模块1：旋转直到球在中心（很成熟，很优秀，很赏心悦目(*¯︶¯*)）
     + 小模块2：运动一定时间，move_t_sec(time,mode,speed)分别对应运动时间，运动模式（0:直行，1:平移，2旋转），和速度
     + 小模块3：make_goal()，利用模块2，后退，冲刺，射门！↖(^ω^)↗
     +  小模块4：数学建模，用球门坐标和球坐标，维护一条直线，返回小狗目标点位以及移动距离。（但是测试出来有点小问题...返回的theta过于小，数量级0.0x，可能是把球当成了目标，并且返回的distance过于大，大约8.x，还需要后续调整）
     + 小模块5：利用socket返回球和狗坐标。目前用简单的调用一次get_dog_address（）方法实现，（感谢whf同学的封装！！后续继续调整）
     +   通过改变rotate.py，形成守门狗的大致思路：与rotate基本一致，z坐标换y坐标。只是还需要后续完善，以便处理球开始时在镜头外的情况。

+ 写了主程序striker.py，基本串联起所有小模块。（目前卡在维护直线的routine函数返回的目标坐标有问题，暂时无法完整射门QWQ）

+ 黑心老板榨取两只狗狗电量都到百分之五以下（bushi

+  大家都好棒，辛苦啦！！
