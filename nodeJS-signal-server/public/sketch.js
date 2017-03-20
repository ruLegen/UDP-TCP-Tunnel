var socket;
var myID;
var servername = "192.168.0.192:8001";

var selfInfo = {
    id:"",
    username: "",
    localAddress:"",
    localPort:"",
    remoteAddress:"",
    remotePort: ""
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
    data.map(function (e) {
      createListItem(e.username,document.querySelector('.collection'))
    })
    $('.progress').animate({opacity: 0},300);
}

function sendTo() {
    socket.emit("sendTo",data);
}

function gotMessage(data) {
    console.log(data);
    alert(data.txt);
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

function createListItem(username,appendTo) {
    var a = document.createElement('a');
    var icon = document.createElement('i');
    var span =     document.createElement('span');
    a.className = "collection-item waves-effect waves-light";
    icon.className = "right material-icons";
    span.className ="title";
    icon.innerText = "grade";
    span.innerText= username;
    a.appendChild(icon);
    a.appendChild(span);
    appendTo.appendChild(a);
}

function renderSelfInfo() {

}