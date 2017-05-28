var express = require('express');
var socket = require('socket.io');
var user = require('user');
var app = express();
var server = app.listen(8000);
	app.use(express.static('public'));
var io = socket(server);
var UserStore = new user.UserStore();

var connectedClients = [];

io.sockets.on('connection',newConnection);


function newConnection(client){
    updateConnectedClients();
    UserStore.addUser(client.id);
    //io.sockets.emit("clients",connectedClients);

    client.on('sendTo',function (data) {
        try {
            this.to(data.id).emit('message',UserStore.findById(client.id));
        }
        catch (e){
            console.log(e)
        }
    });

    client.on("get-clients",function (data) {
       //client.emit("clients",connectedClients);
    });

    client.on('update-info',function (data) {               //Addition new client
        try {
            console.log('registered');
            UserStore.updateUser(client.id,data);
            io.sockets.to(client.id).emit("registered",{name:data.username});//check if this user hasn't take exist name. if took delete from and disconnect him from IO;
        }
        catch(exeption)
        {
             console.log(exeption)
             io.sockets.to(client.id).emit("error",exeption);
            // client.disconnect();
             updateConnectedClients()
        }

    });
    client.on("disconnecting",disconnectClient)
    client.on('get-user',function (data) {

       io.sockets.to(client.id).emit("user-info",UserStore.findAllByName(data.username));
    });
    client.on('update',function (data) {
        UserStore.updateUserWithoutCheck(data.id,data)
        io.sockets.to(data.id).emit('update-self-info',data)
        console.log(data)
    })
    client.on('accept',function (data) {
      io.sockets.to(data.to).emit('connection-accept',data.user)
    })
    client.on('decline',function (data) {
      io.sockets.to(data.to).emit('connection-decline',data.user)
    })

}

function disconnectClient() {

    UserStore.deleteById(this.id)
    updateConnectedClients();
    //io.sockets.emit("clients",connectedClients);
}

function updateConnectedClients() {
   	connectedClients = Object.keys(io.sockets.clients().connected)

}