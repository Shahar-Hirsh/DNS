import socket

def get_IP():
    """
    gets the ip
    :return: ip
    :rtype: str
    """
    while True:
        valid = True
        ans = input("enter an IP - ")
        list_ip = ans.split('.')
        if len(list_ip) == 4:
            for i in list_ip and valid:
                if not i.isdigit() and not int(i) <= 255:
                    valid = False
            if valid:
                break
    return ans


my_sock = socket.socket()
# connect to server
try:
    my_sock.connect(("127.0.0.1",53))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again {str(e)}")

while True:
    msg = input("enter 1 for IP, 2 for HostName and 3 for exit - ")
    if msg == '1':
        ans = get_IP()
    elif msg == '2':
        ans = input("enter HostName - ")
    elif msg == "3":
        break
    else:
        print("invalid input - try again!!!")
        continue

    try:
        my_sock.send(str(len(ans)).encode())
        my_sock.send(msg.encode())
    except Exception as e:
        print(f"error in sending data {str(e)}")
        break


my_sock.close()
print("bye bye")
