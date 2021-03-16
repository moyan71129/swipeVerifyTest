# -*- coding: utf-8 -*-
import os
import cv2   #导入模块，opencv的python模块叫cv2
import time

from mobile import session, size, screenshot, move_actions, switch_actions, touchActions, tap

def image_match(imgPath, buttonImg):
    actions_point = []
    if os.path.isfile(imgPath) is False:
        return actions_point
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
            # cv2.imwrite('img2222.png', out)

            # img[0:375, 240:480]的含义
            # 0: 375指的从竖直方向截取0~375
            # 240: 480指的是从水平方向截取240~480
            start_x = start_button_point_x - 70
            end_x = start_button_point_x + 65
            start_y = start_button_point_y - 370
            end_y = start_button_point_y
            # 根据坐标点截取图片
            small_img = image[start_y:end_y, start_x: end_x]

            cv2.imwrite('small_img.png', small_img)
            img = cv2.imread('small_img.png')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 将BGR格式转换成灰度图片

            ret, binary = cv2.threshold(gray, 100, 150, cv2.THRESH_BINARY)  # 灰度阈值
            # 对binary去噪，腐蚀与膨胀
            binary = cv2.erode(binary, None, iterations=2)
            binary = cv2.dilate(binary, None, iterations=2)
            cv2.imwrite('binary2222.png', binary)
            imgobj = cv2.imread('binary2222.png')  # 读取图像
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
            if total_nums == 0:
                print("查找坐标失败。")
                return
            av_row = int(total_row / total_nums)
            av_col = int(total_col / total_nums)

            out = cv2.rectangle(imgobj, (av_col, av_row),
                                (av_col + 10, av_row), (0, 0, 255), 2)
            cv2.imwrite('img5555.png', out)

            # # 基于原图的坐标点
            icon_x = start_x + av_col
            icon_y= start_y + av_row
            print("icon_x,y  = ", icon_x, icon_y)



            # # 基于原图截取滑动框和目标滑动框图片
            image = cv2.imread(imgPath)  # 读取图像

            out = cv2.rectangle(image, (icon_x, icon_x),
                                (icon_x + 10, icon_y), (0, 0, 255), 2)
            cv2.imwrite('img4444.png', out)

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
            binary = cv2.erode(binary, None, iterations=2)
            binary = cv2.dilate(binary, None, iterations=2)
            cv2.imwrite('binary3.png', binary)

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
                    out = cv2.rectangle(binary, (x + int(w/2), y + int(h/2)), (x + int(w/2), y + int(h/2)), (0, 0, 255), 2)
                    out = cv2.rectangle(out, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.imwrite('img1111.png', out)
                    center_point_x = x + int(w/2)
                    center_point_y = y + int(h/2)

            origin_x = start_x + center_point_x
            origin_y = start_y + center_point_y
            print('origin_x, y', origin_x, origin_y)

            imgobj333 = cv2.imread(imgPath)  # 读取图像
            move_target_point_x = origin_x
            move_target_point_y = start_button_point_y
            move_distance = origin_x - start_button_point_x

            actions_point = move_actions(start_button_point_x/2, start_button_point_y/2, origin_x/2, start_button_point_y/2)
            print(start_button_point_x, start_button_point_y, origin_x, start_button_point_y)
            print(actions_point)

            out = cv2.rectangle(imgobj333, (start_button_point_x, start_button_point_y), ( origin_x, move_target_point_y), (0, 0, 255), 2)
            # out = cv2.rectangle(out, (origin_x, origin_y), ( move_target_point_x, move_target_point_y), (0, 0, 255), 2)
            cv2.imwrite('img3333.png', out)
            # cv2.imshow("test", imgobj333)
            return actions_point

    return actions_point

    # cv2.waitKey(0)  # 等待事件触发，参数0表示永久等待
    # cv2.destroyAllWindows()  # 释放窗口

def image_check(imgPath, buttonImg):
    #  检查弹框是否还存在
    image = cv2.imread(imgPath)  # 读取图像
    template_rgb = cv2.imread(buttonImg)
    res = cv2.matchTemplate(image, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    if len(value) == 4:
        # 最大匹配概率
        print("max match : ", value[1])
        if value[1] > 0.8:
            return False
    return True

def image_refresh(url, session, imgPath, refreshImg):
    #  检查弹框是否还存在
    image = cv2.imread(imgPath)  # 读取图像
    template_rgb = cv2.imread(refreshImg)
    res = cv2.matchTemplate(image, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    if len(value) == 4:
        # 最大匹配概率
        print("max match : ", value)
        if value[1] > 0.8:
            max_point = value[3] # 此处找到的坐标为匹配到的左上角的坐标点，需要将模板图片的长宽的1/2 加到匹配的坐标点才是中心坐标点
            template_size = template_rgb.shape
            template_height = template_size[0]  # 将tuple中的元素取出，赋值给height，width
            template_width = template_size[1]
            start_button_point_x = max_point[0] + int(template_width/2) # 中心坐标点的x坐标点
            start_button_point_y = max_point[1] + int(template_height/2) # 中心坐标点的y坐标点
            print("start_point: ", start_button_point_x, start_button_point_y)

            # out = cv2.rectangle(image, (start_button_point_x, start_button_point_y),(start_button_point_x, start_button_point_y), (0, 0, 255), 2)
            # cv2.imwrite('refreshImg3333.png', out)

            tap(url, session, int(start_button_point_x/2), int(start_button_point_y/2))



if __name__ == '__main__':


    url = "http://localhost:8100"
    session_id = session(url)
    wsize = size(url, session_id)
    imgPath = "test2.jpeg"
    buttonImg = "button.png"
    refreshImg = "refresh.png"

    screenshot(url, session_id, imgPath)

    success = image_check(imgPath, buttonImg)
    if success:
        actions_point = image_match(imgPath, buttonImg)
        actions = switch_actions(actions_point)
        touchActions(url, session_id, {"actions": actions})
    for i in range(3):
        success = image_check(imgPath, buttonImg)
        if success is False:
            # 弹框还存在， 点击刷新，再次识别
            image_refresh(url, session_id, imgPath, refreshImg)
            time.sleep(2)
            screenshot(url, session_id, imgPath)
            actions_point = image_match(imgPath, buttonImg)
            actions = switch_actions(actions_point)
            touchActions(url, session_id, {"actions": actions})
        else:
            break