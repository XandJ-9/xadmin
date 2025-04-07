import socket

def check_port(host, port):
    """
    检查指定主机和端口是否开放

    :param host: 主机地址，例如 '127.0.0.1' 或 'example.com'
    :param port: 端口号，例如 80
    :return: 如果端口开放返回 True，否则返回 False
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # 设置超时时间
        try:
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False