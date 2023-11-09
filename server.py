
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

    def changeType(method,params):
        if method == "floor":
            return float(params)
        elif method == "nroot":
            return int(params)
        elif method == "reverse":
            return str(params)
        elif method == "validAnagram":
            return str(params)
        else:
            return str(params)


def main():
    functionHashmap = {
        "floor": Function.floor,
        "nroot": Function.nroot,
        "reverse": Function.reverse,
        "validAnagram": Function.validAnagram,
        "sort": Function.sort
    }

    sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    server_address = "/tmp/json_rpc_socket.sock"

    try:
        os.unlink(server_address)
    except FileNotFoundError:
        pass

    print("Starting up on {}".format(server_address))

    sock.bind(server_address)

    sock.listen(1)

    while True:
        #connection,client_address = sock.accept()

        try:
            
            while True:
                connection,client_address = sock.accept()
                print("connection from",client_address)

                data = connection.recv(1024)
                data_str = data.decode("utf-8")

                print("Received data: {}".format(data_str))
                

                receivedData = json.loads(data)

                

                method = receivedData["method"]
                params = receivedData["params"]
                id = receivedData["id"]

            
                params = Function.changeType(method,params)

                


                

                if method in functionHashmap:
                    
                    result = functionHashmap[method](params)

                    answer = {
                        "results": result,
                        "id":id
                    }
                    
                else:
                    answer = {
                        "result":result,
                        "id":id
                    }
                

                
                if data:
                    connection.send(json.dumps(answer).encode())
                    print("answer data: {}".format(answer))
                else:
                    print("no data from",client_address)
                    break         
                            

        finally:
            print("Closing current connection")
            connection.close()


if __name__ == "__main__":
    main()
