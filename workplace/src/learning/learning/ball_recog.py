import cv2
import numpy as np


class green_identify(Node):
    '''detect certain color in a image'''
    def __init__(self, color) -> None:
        super().__init__(color)

        self.declare_parameter("dog_name", "az")

        dog_name = self.get_parameter("dog_name").get_parameter_value().string_value

        self.sub = self.create_subscription(Range, f'/{dog_name}/ultrasonic_payload', self.sub_callback, 10)
        pass

    def sub_callback(self, msg: Range):
        '''the callback function of subscriber'''
        dist = msg.range
        self.get_logger().info(f"the distance is {dist}")
    # 灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 转换为HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 二值化处理
    lower_green = np.array([0, 100, 100])
    higher_green = np.array([10, 200, 200])

    mask = cv2.inRange(hsv, lower_green, higher_green)

    # 膨胀操作
    kernel = np.ones([5, 5], dtype=np.uint8)
    dilate = cv2.dilate(mask, kernel, iterations=1)

    # 画出轮廓
    cnts, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # 判断是否有轮廓
    if len(cnts) == 0:

        # 没有即显示原图
        cv2.imshow("red_identify", img)
        return

    max_cnt = max(cnts, key=cv2.contourArea)
    cv2.drawContours(img, max_cnt, -1, (0, 0, 255), 2)

    # 最大外接矩形
    (x, y, w, h) = cv2.boundingRect(max_cnt)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)

    cv2.imshow("red_identify", img)


if __name__ == "__main__":
    main()

def main():
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        get_logger().info('Can\'t open camera!')
    # 设置摄像头参数，3和4为像素大小，5为帧率
    cap.set(3, 256)
    cap.set(4, 256)
    cap.set(5, 60)

    while True:

        # 循环读取每一帧
        flag, frame = cap.read()

        #  读取失败
        if not flag:
            print("Camera error!")
            break

        # 调用颜色识别
        green_identify(frame)

        # 若没有按下q键，则每10毫秒显示一帧（OxFF为"q"的ASCII码）
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
