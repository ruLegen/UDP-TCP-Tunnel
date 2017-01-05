var http = require('http');
var Users = {};
function User(name,ip,port) {
    this.username = name;
    this.userip = ip;
    this.userport = port;

}
function getRequestBody(request,fn) {
var body = [];
    request.on('data', function(chunk) {
        body.push(chunk);
    }).on('end', function() {
        body = Buffer.concat(body).toString();
        fn(body);
        // at this point, `body` has the entire request body stored in it as a string
    });
}
function parsePOST (body) {
    console.log(body)
    var list = {},
        rc = body.toString();
        rc && rc.split('&').forEach(function( cookie ) {
            var parts = cookie.split('=');
            list[parts.shift().trim()] = decodeURI(parts.join('='));
         });

    return list;
}


function Router(request,text,to,arg) {
    if(request.url == text)
    {
        to(arg);
    }
}

function RegUser(params) {
    var request = params['request'];
    var response = params['response'];
     getRequestBody(request,function (_data) {
         var POST = parsePOST(_data);
         var username = POST['username'];
         var userip = POST['userip'];
         var userport = POST['userport'];
         if(Users[username] == undefined)
         {

            Users[username] = new User(username,userip,userport);
             response.writeHead(200, {'Content-Type': 'application/json'});
             response.write('1');
             response.end();
             console.log('User rigistered ' +
                            'Username '+ username +
                            'IP '+ userip +
                             'Port' + userport   );

         }
         else
         {
             response.writeHead(200, {'Content-Type': 'application/json'});
             response.write('0');
             response.end();
             console.log('USer not rigistred' + username);

         }
        return 0;
    });

}
function ViewUser(params) {
    var request = params['request'];
    var response = params['response'];

     getRequestBody(request,function (_data) {
         var POST = parsePOST(_data);
         var username = POST['username'];
        console.log(Users[username]);

        if(Users[username] == undefined)
        {
            response.writeHead(200, {'Content-Type': 'application/json'});
            response.write('{}');
            response.end();
        }
        else
        {
            response.writeHead(200, {'Content-Type': 'application/json'});
            response.write(JSON.stringify(Users[username]).toString());
            response.end();

        }
    });

}
function UpdateUser(params) {
    var request = params['request'];
    var response = params['response'];

     getRequestBody(request,function (_data) {
         var POST = parsePOST(_data);
         var username = POST['username'];
         var userip = POST['userip'];
         var userport = POST['userport'];
         if(Users[username] == undefined)
        {
            response.writeHead(200, {'Content-Type': 'application/json'});
            response.write('0');
            response.end();
        }
        else
        {
            Users[username].ip = userip;
            Users[username].port = userport;
            response.writeHead(200, {'Content-Type': 'application/json'});
            response.write('1');
            response.end();

        }
    });

}
http.createServer(function (request, response) {

    Router(request,"/reguser",RegUser,{'request':request,'response':response});
    Router(request,"/viewuser",ViewUser,{'request':request,'response':response});
    Router(request,"/updateuser",UpdateUser,{'request':request,'response':response});


}).listen(8001);

console.log('Server running at http://127.0.0.1:8001/');