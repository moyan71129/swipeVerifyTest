import requests
import base64
import random
import json

def session(url):
    # 获取session
    headers = {'content-type': 'application/json'}
    postdata = """{"capabilities" : {"bundleId":"com.apple.mobilesafari"}}"""
    url = url + '/session'
    result = requests.post(url, data=postdata, headers=headers)
    print(result.text)
    res = None
    sessionId = None
    if result != None:
        try:
            res = result.json()
        except:
            res = None
    if res != None:
        sessionId = res.get("sessionId")
        print("sessionId = ", sessionId)
    return sessionId

def touchActions(url, session, actions):
    # 移动点击
    headers = {'content-type': 'application/json'}
    # postdata = """{"actions":[{"action":"press","options":{"x":150,"y":500}},{"action":"wait","options":{"ms":1330}},{"action":"moveTo","options":{"x":150,"y":600}},{"action":"wait","options":{"ms":1330}},{"action":"moveTo","options":{"x":250,"y":600}},{"action":"release","options":{}}]}"""
    postdata = '%s'%json.dumps(actions)
    print("-----------")
    print(postdata)
    url = url + "/session/" + session + '/wda/touch/multi/perform'
    r = requests.post(url, data=postdata, headers=headers)
    print(r.text)

def size(url, session):
    # 屏幕尺寸
    headers = {'content-type': 'application/json'}
    url = url + "/session/" + session + '/window/size'
    result = requests.get(url, headers=headers)
    print(result.text)
    res = None
    size = {}
    if result != None:
        try:
            res = result.json()
        except:
            res = None
    if res != None:
        size = res.get("value")
        print("size = ", size)
    return size

def screenshot(url, session, png_filename):
    # 截图
    headers = {'content-type': 'application/json'}
    url = url + "/session/" + session + '/screenshot'
    result = requests.get(url, headers=headers)
    res = None
    if result != None:
        try:
            res = result.json()
        except:
            res = None
    if res != None:
        raw_value = base64.b64decode(res.get("value"))
        png_header = b"\x89PNG\r\n\x1a\n"
        if not raw_value.startswith(png_header) and png_filename:
            print(-1, "screenshot png format error")
        if png_filename:
            with open(png_filename, 'wb') as f:
                f.write(raw_value)



def move_actions(start_x, start_y, end_x, end_y):
    count_move = random.randint(10, 30)
    actions_point = []
    start_x = start_x
    start_y = start_y
    for i in range(count_move - 1): # 移动次数
        count_point = random.randint(1, 5)
        count_sleep = random.randint(1, 5)
        point = (start_x, start_y)
        if start_x < end_x:
            actions_point.append(point)
        else:
            break
        start_x = start_x + count_point
        start_y = start_y + count_sleep
    actions_point.append((end_x, end_y))
    return actions_point

def switch_actions(actions_point):
    actions = []
    for point in actions_point:
        if actions_point.index(point) == 0:
            # 按下
            actions.append({r"action": "press", "options": {"x": point[0], "y": point[1]}})
            actions.append({r"action": "wait", "options": {"ms": 1120}})
        elif actions_point.index(point) == len(actions_point):
            # 释放
            actions.append({"action": "wait", "options": {"ms": 1400}})
            actions.append({"action": "release", "options": {}})
            break
        else:
            actions.append({"action": "moveTo", "options": {"x": point[0], "y": point[1]}})
            actions.append({"action": "wait", "options": {"ms": 152}})
    print(str(actions))
    return actions

def tap(url, session, point_x, point_y):
    # 点击刷新
    actions = [{r"action": "press", "options": {"x": point_x, "y": point_y}}, {"action": "wait", "options": {"ms": 100}}, {"action": "wait", "options": {"ms": 90}}]
    touchActions(url, session, {"actions": actions})

# actions_point = move_actions(298, 640, 498, 640)
# actions = switch_actions(actions_point)
# url = "http://localhost:8100"
# session_id = session(url)
# # size = size(url, session)
# # screen_png = "test.png"
# # screenshot(url, session, screen_png)
# touchActions(url, session, {"actions": actions})
# tap(url, session_id, 103, 978/2)
# image = cv2.imread(screen_png)  # 读取图像
# size = image.shape
# print(size)






