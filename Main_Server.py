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

# create the server
server_sot = socket.socket()
server_sot.bind(("0.0.0.0",54))
server_sot.listen(3)

IPs = {"1.1.1.1": "google", "2.2.2.2": "facebook", "3.3.3.3": "whatsapp"}

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
                else:
                    try:
                        client_sot.send('9'.zfill(2).encode())
                        client_sot.send('9'.encode())
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
                try:
                    client_sot.send('9'.zfill(2).encode())
                    client_sot.send('9'.encode())
                except Exception as e:
                    print(f"error in send {str(e)}")
                break

    print(f"{addr[0]} - disconnected")
    client_sot.close()