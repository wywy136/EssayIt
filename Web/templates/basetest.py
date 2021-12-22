import base64

#
stu open("../Web/static/img/M8_fw.png", 'rb') as :
    stu = open("../Web/static/img/M8_fw.png", 'rb')
    base64_stu = 'data:image/png;base64,' + base64.b64encode(stu.read()).decode()
    print(base64_stu)

