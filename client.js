
const net = require("net")
const server_address = "/tmp/json_rpc_socket.sock"

const client = new net.Socket()

const request = {
    method: "",
    params: "",
    id: ""
};


function readUserInput(question) {
    const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
    });

    return new Promise((resolve, reject) => {
        readline.question(question, (answer) => {
            resolve(answer);
            readline.close();
        });
    });
}


(async function main() {

    method = await readUserInput('Input Method --> ');
    params = await readUserInput('Input params --> ');
    id = await readUserInput('Input Id --> ');

    request.method = method == ""? request.method : method;
    request.params = params == ""? request.params : params;
    request.id = id == ""? request.id : id;

    console.log(request);
    
    
    client.connect(server_address, () => {
        console.log('Connected to server');
        
        
        client.write(JSON.stringify(request));
    });
    
    
    client.on('data', (data) => {
        const response = JSON.parse(data);
        
        if (response.error) {
            console.error('Error:', response.error);
        }else{
            console.log(response);
        }
        
        
        client.end();
    });
    
    client.on('close', () => {
        console.log('Connection closed');
    });
    
    
    client.on('error', (error) => {
        console.error('Error:', error);
    });
    
})();
