import socket

def check_IP(ip):
    """
    checks if the ip is valid
    :param ip: the ip to check
    :type ip: str
    :return: if the ip is valid
    :rtype: Bool
    """
    valid = True
    list_ip = ip.split('.')
    if len(list_ip) == 4:
        for i in list_ip:
            if not i.isdigit() or not int(i) <= 255:
                valid = False
                break
    else:
        valid = False
    return valid

server_sot = socket.socket()
server_sot.bind(("0.0.0.0", 53))
server_sot.listen(3)

IPs = {"1.1.1.1": "google", "2.2.2.2": "facebook"}

while True:
    #server waits fo clients
    client_sot, addr = server_sot.accept()
    print(f"{addr[0]} - connected")
    while True:
        try:
            data_len = int(client_sot.recv(2).decode())
            data = client_sot.recv(data_len).decode().split(',')
        except Exception as e:
            print(f"error in recv {str(e)}")
            break

        if data[-1] == "1":
            if check_IP(data[0]):
                if data[0] in IPs.keys():
                    try:
                        client_sot.send(str(len(IPs[data[0]])).zfill(2).encode())
                        client_sot.send(IPs[data[0]].encode())
                    except Exception as e:
                        print(f"error in send {str(e)}")
                    break
                my_sock = socket.socket()
                # connect to server
                try:
                    my_sock.connect(("127.0.0.1", 54))
                except Exception as e:
                    my_sock.close()
                    print(f"server is down - try again {str(e)}")
                    break

                try:
                    my_sock.send(str(len(data[0]) + 2).zfill(2).encode())
                    my_sock.send((data[0] + "," + data[-1]).encode())
                except Exception as e:
                    print(f"error in sending data {str(e)}")
                    break

                try:
                    server_data_len = int(my_sock.recv(2).decode())
                    server_data = my_sock.recv(server_data_len).decode()
                except Exception as e:
                    print(f"error in sending data {str(e)}")
                    break

                if server_data != '9':
                    IPs[data[0]] = server_data

                try:
                    client_sot.send(str(len(server_data)).zfill(2).encode())
                    client_sot.send(server_data.encode())
                except Exception as e:
                    print(f"error in send {str(e)}")
                break

            else:
                break
        else:
            key = None
            for k, val in IPs.items():
                if val == data[0]:
                    key = k
                    try:
                        client_sot.send(str(len(k)).zfill(2).encode())
                        client_sot.send(k.encode())
                    except Exception as e:
                        print(f"error in send {str(e)}")
                    break
            if not key:
                my_sock = socket.socket()
                # connect to server
                try:
                    my_sock.connect(("127.0.0.1", 54))
                except Exception as e:
                    my_sock.close()
                    print(f"server is down - try again {str(e)}")
                    break

                try:
                    my_sock.send(str(len(data[0]) + 2).zfill(2).encode())
                    my_sock.send((data[0] + "," + data[-1]).encode())
                except Exception as e:
                    print(f"error in sending data {str(e)}")
                    break

                try:
                    server_data_len = int(my_sock.recv(2).decode())
                    server_data = my_sock.recv(server_data_len).decode()
                except Exception as e:
                    print(f"error in sending data {str(e)}")
                    break

                if server_data != '9':
                    IPs[server_data] = data[0]

                try:
                    client_sot.send(str(len(server_data)).zfill(2).encode())
                    client_sot.send(server_data.encode())
                except Exception as e:
                    print(f"error in send {str(e)}")
                break

    print(f"{addr[0]} - disconnected")
    client_sot.close()