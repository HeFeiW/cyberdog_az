def get_dog_address():
    ip = '10.0.0.143' # 查看上位机ip，进行修改
    client_socket = socket.socket()
    client_socket.connect((ip, 40000))
    msg = 'start'
    while True:
        client_socket.send(msg.encode())
        data = client_socket.recv(1024).decode()
        result = parse_data(data)
        if result is not False:
            return result

def parse_data(data):
    # split方法用于按空格分隔字符串
    a, b, c, d = data.split(' ')
    # 将字符串转换为浮点数，如果字符串为'None'，则返回None
    a = float(a) if a != 'None' else None
    b = float(b) if b != 'None' else None
    c = float(c) if c != 'None' else None
    d = float(d) if d != 'None' else None
    # 如果任何一个坐标是None，返回False
    if a is None or b is None or c is None or d is None:
        return False
    # 返回两个坐标
    return (a, b), (c, d)

def main():
    dog_coords, ball_coords = get_dog_address()
    print(dog_coords, ball_coords)
if __name__ == '__main__':
    main()