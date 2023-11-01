
import socket
import os
import json
import math

class Function:
    def floor(x):
        return math.floor(x)

    def nroot(n,x):
        return math.floor(x**(1/n))

    def reverse(s):
        return s[::-1]

    def validAnagram(str1,str2):
        return sorted(str1) == sorted(str2)

    def sort(strArr):
        return sorted(strArr)
    
    def checkType(answer):
        if isinstance(answer,bool):
            return "bool"
        elif isinstance(answer,int):
            return "int"
        elif isinstance(answer,float):
            return "float"
        elif isinstance(answer,str):
            return "str"
        elif isinstance(answer,list):
            return "list"
        else:
            return "incorrect type"


def main():
    functionHashmap = {
        "floor": Function.floor,
        "nroot": Function.nroot,
        "reverse": Function.reverse,
        "validAnagram": Function.validAnagram,
        "sort": Function.sort
    }

    sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    server_address = "127.0.0.1"
    try:
        os.unlink(server_address)
    except FileNotFoundError:
        pass

    print("Starting up on {}".format(server_address))

    sock.bind(server_address)

    sock.listen(1)

    connection,client_address = sock.accept()

    while True:
        connection,client_address = sock.accept()

        try:
            print("connection from",client_address)

            while True:
                data = connection.recv(1024)
                data_str = data.decode("utf-8")

                print("Received data: {}".format(data_str))

                receivedData = json.loads(data)
                method = receivedData["method"]
                params = receivedData["params"][1:-1].split(",")

                if functionHashmap[method]:
                    result = functionHashmap[method](params)
                    resultType = Function.checkType(result)

                    answer = {
                        "result":result,
                        "result_type": resultType,
                        "id":receivedData["id"]
                    }
                else:
                    answer = {
                        "result":"incorrect method",
                        "result_type": "...",
                        "id":receivedData["id"]
                    }
                if data:
                    connection.sendall(json.dumps(answer).encode())
                else:
                    print("no data from", client_address)
                    break
                
                
        finally:
            print("Closing current connection")
            connection.close()


if __name__ == "__main__":
    main()