var express = require('express');
var socket = require('socket.io');
var user = require('user');

var app = express();
var server = app.listen(8002);
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
        setIntervald(function () {
//                 client.to(data.id).emit('message',{});
                  io.to(client.id).emit('message',{});

        },1000);

    });

    client.on("get-clients",function (data) {
       //client.emit("clients",connectedClients);
    });

    client.on('update-info',function (data) {               //Addition new client
        try {
            console.log('registered');
            console.log(data);
            UserStore.updateUser(client.id,data);
            io.sockets.to(client.id).emit("registered",{name:data.username});//check if this user hasn't take exist name. if took delete from and disconnect him from IO;
        }
        catch(exeption)
        {

             console.log(exeption + "ERROROROROROR")
             io.sockets.to(client.id).emit("error",exeption);
            // client.disconnect();
             updateConnectedClients()
        }

    });
    client.on("disconnecting",disconnectClient)
    client.on('get-user',function (data) {
        console.log("get-data");

       io.sockets.to(client.id).emit("user-info",UserStore.findAllByName(data.username));
        console.log(UserStore.findAllByName(data.username))
    });
}

function disconnectClient() {

    UserStore.deleteById(this.id)
    updateConnectedClients();
    //io.sockets.emit("clients",connectedClients);
}

function updateConnectedClients() {
   	connectedClients = Object.keys(io.sockets.clients().connected)

}