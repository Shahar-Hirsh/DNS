import socket

def get_IP():
    """
    gets the ip
    :return: ip
    :rtype: str
    """
    ans = input("enter an IP - ")
    while True:
        valid = True
        list_ip = ans.split('.')
        if len(list_ip) == 4:
            for i in list_ip:
                if not i.isdigit() or not int(i) <= 255:
                    valid = False
                    break
            if valid:
                break
        ans = input("invalid IP - try again: ")

    return ans


IPs = {"1.1.1.1": "google"}
my_sock = None
while True:
    msg = input("enter 1 for IP, 2 for HostName and 3 for exit - ")
    if msg == '1':
        ans = get_IP()
        if ans in IPs.keys():
            print("the HostName for the IP - "+ans+" is: "+IPs[ans])
        else:
            my_sock = socket.socket()
            # connect to server
            try:
                my_sock.connect(("127.0.0.1", 53))
            except Exception as e:
                my_sock.close()
                print(f"server is down - try again {str(e)}")
                continue

            try:
                my_sock.send(str(len(ans)+2).zfill(2).encode())
                my_sock.send((ans+","+msg).encode())
            except Exception as e:
                print(f"error in sending data {str(e)}")
                continue

            try:
                data_len = int(my_sock.recv(2).decode())
                data = my_sock.recv(data_len).decode()
            except Exception as e:
                print(f"error in sending data {str(e)}")
                continue
            if data == '9':
                print("there is not an HostName for the IP - " + ans)
                continue
            IPs[ans] = data
            print("the HostName for the IP - "+ans+" is: "+IPs[ans])

    elif msg == '2':
        ans = input("enter HostName - ")
        key = None
        for k, val in IPs.items():
            if val == ans:
                key = k
                print("the IP for the HostName - " + ans + " is: " + key)
                break
        if not key:
            my_sock = socket.socket()
            # connect to server
            try:
                my_sock.connect(("127.0.0.1", 53))
            except Exception as e:
                my_sock.close()
                print(f"server is down - try again {str(e)}")
                continue

            try:
                my_sock.send(str(len(ans) + 2).zfill(2).encode())
                my_sock.send((ans + "," + msg).encode())
            except Exception as e:
                print(f"error in sending data {str(e)}")
                continue

            try:
                data_len = int(my_sock.recv(2).decode())
                data = my_sock.recv(data_len).decode()
            except Exception as e:
                print(f"error in sending data {str(e)}")
                continue

            if data == '9':
                print("there is not an IP for the HostName - " + ans)
                continue
            IPs[data] = ans
            print("the IP for the HostName - " + ans + " is: " + data)

    elif msg == "3":
        break
    else:
        print("invalid input - try again!!!")
        continue

if my_sock:
    my_sock.close()
print("bye bye")
