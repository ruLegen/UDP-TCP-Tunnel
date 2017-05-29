var socket;
var myID;
var servername = window.location.host;
//var servername ="http://d2834146.ngrok.io"
var searchedUsers;
var currentUser;
var stunUpdated = false
var lastmodalID = 0;
var selfInfo = {
    id:"",
    username: "",
    localAddress:"",
    localPort:"",
    remoteAddress:"",
    remotePort: ""
}
$(window).on('beforeunload', function(){
    socket.close();
});
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

$(document).ready(function()
{
   socket = io.connect(servername);
     socket.on('message',gotMessage);            //when message is comming
    socket.on('connect',connected);             //what to do when connected to server
    socket.on('user-info',remoteUserInfo);      //when getting info about user
    socket.on('error',onRegisterError);             //when comming some error from server
    socket.on('disconnect',lostConnection);     //when user disconnected from server
    socket.on('registered',onRegister);
    socket.on('update-self-info',selfInfoUpdate)
    socket.on('connection-accept',connectionAccept)
    socket.on('connection-decline',connectionDecline)

});

function connectionAccept(data) {
       Materialize.toast("Запрос принят ("+data.username+")",4000,"green");
     args = "--directconnection"+
            " --sourceport " + selfInfo.localPort+
            " --sourcehost " + selfInfo.localAddress +
            " --remotehost " + data.remoteAddress +
            " --remoteport " + data.remotePort
    stunFrame = document.createElement('iframe');
    stunFrame.src = "tunnel://"+args;
    stunFrame.id="STUN_FRAME";
    stunFrame.width = "1";
    console.log("tunnel://"+args)

    $('#info-block').append(stunFrame);
    $(stunFrame).remove();
}
function connectionDecline(data) {
     Materialize.toast("Запрос отклонен ("+data.username+")",4000,"red");
}

function selfInfoUpdate(data) {
    console.log(data)
    selfInfo = data;
    stunUpdated = true;
    renderSelfInfo()
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
    var from = data;
    console.log(data)
    createModal("Запрос от "+from.username,"Хотите подключиться к нему?",function () {
        socket.emit('accept',{to:from.id,user:selfInfo});
        connectionAccept(data)
    },function () {
        socket.emit('decline',{to:from.id,user:selfInfo});
    });

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
            if(stunUpdated)
                sendTo(currentUser);
            else
                Materialize.toast("Обновите свои настройки",4000,"red");
        });
        $('#update-stun').click(function () {
            updateStun()

        });
    });

    Materialize.toast("Good Job, you are registered",4000,"green");

}
function lostConnection() {
    
}
function updateStun() {
    port = prompt("Which port do u like to pin?")

    args = "--username "+ selfInfo.username+
            " --action " + "stun"+
            " --server " + servername +
            " --localport " + port +
            " --id " + selfInfo.id
    stunFrame = document.createElement('iframe');
    stunFrame.src = "webhandler://"+args;
    stunFrame.id="STUN_FRAME";
    stunFrame.width = "1";
    $('#info-block').append(stunFrame);
    $(stunFrame).hide();



    //window.assign(link.href)
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


function createModal(header,text,onagree,ondisagree) {
    var modalWraper = document.createElement('div');
        modalWraper.id = "wraper"+lastmodalID;

    var modal = document.createElement('div');
        modal.id = "modal"+lastmodalID;
        modal.className = "modal";
    var modalContent = document.createElement('div');
        modalContent.className = "modal-content";
    var modalHeader = document.createElement("h4")
        modalHeader.textContent = header;
    var modalText = document.createElement("p");
        modalText.textContent = text;
    var modalFooter = document.createElement('div');
        modalFooter.className = "modal-footer";
    var agree = document.createElement('a');
        agree.onclick = onagree;
        agree.textContent = "Да"
    var disagree = document.createElement('a');
        disagree.onclick = ondisagree;
        disagree.textContent = "Нет"
    agree.className = "modal-action modal-close waves-effect waves-green btn-flat";
    disagree.className = "modal-action modal-close waves-effect waves-green btn-flat";

    modalFooter.appendChild(disagree);
    modalFooter.appendChild(agree);

    modalContent.appendChild(modalHeader);
    modalContent.appendChild(modalText);


    modal.appendChild(modalContent);
    modal.appendChild(modalFooter);
    modalWraper.appendChild(modal)
    $(modal).modal();
    $(modal).modal('open');
    $('#info-block').append(modalWraper)
    return modalWraper
}