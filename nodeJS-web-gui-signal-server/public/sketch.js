var socket;
var myID;
var servername = "localhost:8001";
//var servername ="http://d2834146.ngrok.io"
var searchedUsers;
var currentUser;

var selfInfo = {
    id:"",
    username: "",
    localAddress:"",
    localPort:"",
    remoteAddress:"",
    remotePort: ""
}

var translatedInfo ={
    id:"ID",
    username: "Имя",
    localAddress:"Локальный Адресс",
    localPort:"Локальный Порт",
    remoteAddress:"Адресс",
    remotePort: "Порт",
    status:"Статус",
    connected:"Подключен",
    disconnected:"Отключен",

}


function setup() {

    socket = io.connect(servername);
    socket.on('message',gotMessage);            //when message is comming
    socket.on('connect',connected);             //what to do when connected to server
    socket.on('user-info',remoteUserInfo);      //when getting info about user
    socket.on('error',onRegisterError);             //when comming some error from server
    socket.on('disconnect',lostConnection);     //when user disconnected from server
    socket.on('registered',onRegister);

}



function remoteUserInfo(data) {
    $('.progress').animate({opacity: 1},400);
    $('.collection').empty();
    searchedUsers = data;
    $('.progress').animate({opacity: 0},300);
    data.map(function (element,index) {
      createListItem(element.username,index,document.querySelector('.collection'))
    });
    $('.remote-user-item').on('click',renderRemoteInfo);


}

function sendTo(data) {
    socket.emit("sendTo",data);
}

function gotMessage(data) {
Materialize.toast("Юзер "+data.username + "упомянул вас",1500,"green");

}
function connected(data) {
        myID = this.id;
        selfInfo.id= myID;
    console.log(selfInfo)

}

function onRegisterError(data) {

    $('.progress').animate({opacity: 0},900);
    Materialize.toast("Username "+data.username+" is already exist",4000,"amber darken-4 white-text");
}
function onRegister(data) {

    var socket = this;
    $('.progress').animate({opacity: 0},900);
    $('#reg-block').fadeOut(500,function () {
        $('#info-block').show(100);
        $('#search').click(function () {
            var user = $('#nickname').val();
            var data = {username:user}
            socket.emit('get-user',data);

        });
        renderSelfInfo();
        $('#send-button').click(function () {
            sendTo(currentUser);
        });
    });

    Materialize.toast("Good Job, you are registered",4000,"green");

}
function lostConnection() {
    
}

function register() {
    var username= $('#text').val();
    if(username != "")
    {
        $('.progress').animate({opacity: 1},400);
        selfInfo.username = username;
        socket.emit('update-info',selfInfo);
    }
    else
    {
        Materialize.toast("Name couldn't be empty",2000,"red darken-1 white-text");
    }


}

function createListItem(username,index,appendTo) {
    var a = document.createElement('a');
    var icon = document.createElement('i');
    var span =     document.createElement('span');
    a.className = "collection-item waves-effect waves-light remote-user-item";
    a.setAttribute('index',index);
    icon.className = "right material-icons";
    span.className ="title";
    icon.innerText = "grade";
    span.innerText= username;
    a.appendChild(icon);
    a.appendChild(span);
    appendTo.appendChild(a);
}

function renderSelfInfo() {
    $('#self-container').empty();
    $('#self-username').text(selfInfo.username);
    for(var item in selfInfo)
    {
        if(item == "username")
            continue;
        var div = document.createElement('div');
        div.className="colletion-item truncate";
        div.innerHTML=translatedInfo[item] + " " + selfInfo[item];
        $('#self-container').append(div);
    }
}
function renderRemoteInfo() {
    var item = this;
    var index = $(item).attr('index');
    var userData = searchedUsers[index];
        currentUser = userData;
    $('#remote-user-container').empty();
    $('#remote-username').text(userData.username);
    for(var item in userData)
    {
        if(item == "username")
            continue;
        var div = document.createElement('div');
        div.className="colletion-item truncate";
        div.innerHTML=translatedInfo[item] + " " + userData[item];
        $('#remote-user-container').append(div);
    }



}