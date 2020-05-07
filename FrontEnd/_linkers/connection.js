function getClima() {
    var {PythonShell} = require("python-shell")
    var path = require("path")

    var opcoes = {
        scriptPath : path.join(__dirname, '../')
    }

    var clima = new PythonShell('quickstart.py', opcoes);

    clima.on('message', function(message) {
        swal(message);
    })
}
function saveBase() {
    var {PythonShell} = require("python-shell")
    var path = require("path")

    var user = document.getElementById("inputUser").value
    var pw = document.getElementById("inputPassword").value
    var host = document.getElementById("inputHost").value
    var port = document.getElementById("inputPort").value
    var db = document.getElementById("inputDatabase").value

    var opcoes = {
        scriptPath : path.join(__dirname, '../../BackEnd'),
        args : [user, pw, host, port, db]
    }

    var credent = new PythonShell('save.py', opcoes);

    credent.on('message', function(message) {
        swal(message);
    })
}

document.getElementById('buttom-bd').addEventListener('click', loadBase);

function loadBase() {
    fetch('credentials.txt').then(function(response) {
        return response.text();
    }).then(function(data){
        console.log(data);
        document.getElementById('test').innerText = data;
    })
}