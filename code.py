# -*- coding: utf-8 -*-
# @Date:2021/3/10 2:09

import os
import cv2   #导入模块，opencv的python模块叫cv2
import random

def move_actions(start_x, start_y, end_x, end_y):
    count_move = random.randint(2, 5)
    count_point = random.randint(10, 20)
    actions_point = []
    start_x = start_x
    start_y = start_y
    for i in range(count_move - 1): # 移动次数
        count_point = random.randint(10, 20)
        count_sleep = random.randint(1, 5)
        point = (start_x, start_y)
        actions_point.append(point)
        start_x = start_x + count_point
        start_y = start_y + count_sleep
    actions_point.append((end_x, end_y))
    return actions_point


def image_match(imgPath, buttonImg):
    if os.path.isfile(imgPath) is False:
        print("file is not exist.")
        return
    image = cv2.imread(imgPath)  # 读取图像
    size = image.shape
    print(size)
    template_rgb = cv2.imread(buttonImg)
    res = cv2.matchTemplate(image, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    if len(value) == 4:
        # 最大匹配概率
        print("max match : ", value[1])
        if value[1] > 0.8:
            #  最大概率大于0.8即认为找到
            max_point = value[3] # 此处找到的坐标为匹配到的左上角的坐标点，需要将模板图片的长宽的1/2 加到匹配的坐标点才是中心坐标点
            template_size = template_rgb.shape
            template_height = template_size[0]  # 将tuple中的元素取出，赋值给height，width
            template_width = template_size[1]
            start_button_point_x = max_point[0] + int(template_width/2) # 中心坐标点的x坐标点
            start_button_point_y = max_point[1] + int(template_height/2) # 中心坐标点的y坐标点
            print("start_point: ", value[3])
            # 输出测试文件，查看找到的坐标点是否正确
            # out = cv2.rectangle(image, (start_button_point_x, start_button_point_y), (start_button_point_x + 10, start_button_point_y), (0, 0, 255), 2)
            # cv2.imwrite('img2222.jpg', out)

            # img[0:375, 240:480]的含义
            # 0: 375指的从竖直方向截取0~375
            # 240: 480指的是从水平方向截取240~480
            start_x = start_button_point_x - 90
            end_x = start_button_point_x + 90
            start_y = start_button_point_y - 600
            end_y = start_button_point_y
            # 根据坐标点截取图片
            small_img = image[start_y:end_y, start_x: end_x]

            cv2.imwrite('small_img.jpg', small_img)
            img = cv2.imread('small_img.jpg')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 将BGR格式转换成灰度图片

            ret, binary = cv2.threshold(gray, 100, 150, cv2.THRESH_BINARY)  # 灰度阈值
            # 对binary去噪，腐蚀与膨胀
            binary = cv2.erode(binary, None, iterations=2)
            binary = cv2.dilate(binary, None, iterations=2)
            cv2.imwrite('binary2222.jpg', binary)
            imgobj = cv2.imread('binary2222.jpg')  # 读取图像
            height = imgobj.shape[0]  # 将tuple中的元素取出，赋值给height，width，channels
            width = imgobj.shape[1]
            channels = imgobj.shape[2]
            total_row = 0
            total_col = 0
            total_nums = 0
            for row in range(height):  # 遍历每一行
                for col in range(width):  # 遍历每一列
                    for channel in range(channels):  # 遍历每个通道（三个通道分别是BGR）
                        if row > 50 and col > 50:
                            (b, g, r) = imgobj[row][col]
                            if b == 0 and g == 0 and r == 0:
                                total_row += row
                                total_col += col
                                total_nums += 1

            av_row = int(total_row / total_nums)
            av_col = int(total_col / total_nums)

            # # 基于原图的坐标点
            icon_x = start_x + av_col
            icon_y= start_y + av_row
            print("icon_x,y  = ", icon_x, icon_y)

            # # 基于原图截取滑动框和目标滑动框图片
            image = cv2.imread(imgPath)  # 读取图像
            width = image.shape[1]
            height = image.shape[0]
            print("test2 height:%s,width:%s" % (height, width))
            start_x = int(icon_x) - 100
            end_x = int((icon_x + 600))
            start_y = int((icon_y - 100))
            end_y = int((icon_y + 100))
            print(start_y, end_y, start_x, end_x)
            img = image[start_y:end_y, start_x: end_x]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(gray, 100, 150, cv2.THRESH_BINARY)  # 灰度阈值
            # 对binary去噪，腐蚀与膨胀
            binary = cv2.erode(binary, None, iterations=4)
            binary = cv2.dilate(binary, None, iterations=2)
            cv2.imwrite('binary3.jpg', binary)

            # contours是轮廓本身，hierarchy是每条轮廓对应的属性。
            # cv2.RETR_TREE建立一个等级树结构的轮廓。cv2.CHAIN_APPROX_SIMPLE矩形轮廓只需4个点来保存轮廓信息
            _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            center_point_x = 0
            center_point_y = 0
            min_num = 50 # 轮廓大小限制，必须大于50
            for contour in contours[1:]:
                x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
                if w > min_num and h > min_num and x > 50:
                    print('find box', x, y, w, h)
                    out = cv2.rectangle(img, (x + int(w/2), y + int(h/2)), (x + int(w/2), y + int(h/2)), (0, 0, 255), 2)
                    cv2.imwrite('img1111.jpg', out)
                    center_point_x = x + int(w/2)
                    center_point_y = y + int(h/2)

            origin_x = start_x + center_point_x
            origin_y = start_y + center_point_y
            print('origin_x, y', origin_x, origin_y)

            imgobj333 = cv2.imread('img2222.jpg')  # 读取图像
            move_target_point_x = origin_x
            move_target_point_y = start_button_point_y
            move_distance = origin_x - start_button_point_x

            out = cv2.rectangle(imgobj333, (start_button_point_x, start_button_point_y), ( move_target_point_x, move_target_point_y), (0, 0, 255), 2)
            out = cv2.rectangle(out, (origin_x, origin_y), ( move_target_point_x, move_target_point_y), (0, 0, 255), 2)
            cv2.imwrite('img3333.jpg', out)
            cv2.imshow("test", imgobj333)

    cv2.waitKey(0)  # 等待事件触发，参数0表示永久等待
    cv2.destroyAllWindows()  # 释放窗口

if __name__ == '__main__':
    imgPath = 'test2.jpeg'
    buttonImg = "button.jpeg"
    image_match(imgPath, buttonImg)
    # print(move_actions(120, 500, 200, 500))