
// issue an xml http request using:
// method - GET, POST, PUT or DELETE
// url - the url
//
// after completing:
// 1. received data is interpreted and parsed as json
// 2. one of two callback functions is called:
//    if status == 200: successhandler(parsed_data)
//    else: errorhandler(statuscode, parsed_data)
//
function ajax(method, url, body, successhandler, errorhandler, credentials) {
    oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function () {
        var data = JSON.parse(oReq.responseText);
        if (oReq.status == 200) {
            successhandler && successhandler(data); // call successhandler if given
        } else if (oReq.status == 401) {  // handle 401
            authinfo = oReq.getResponseHeader("WWW-Authenticate").split(" ");
            if (authinfo[0]!="RestBasic") {  // our own Auth method
                document.querySelector("body").innerHTML="Error: Don't know how to handle Auth Type "+authinfo[0];
            } else {
                render("login");  // show login form
            }
        } else {
            errorhandler && errorhandler(oReq.status, data);
        }
    });
    oReq.open(method, url);
    if (theCredentials) {  // user provided credentials, so include them to request
        oReq.setRequestHeader("Authorization", "RestBasic "+ btoa(theCredentials['username']+":"+theCredentials['password']));
    }
    if (method == 'POST' || method == 'PUT') {
        oReq.setRequestHeader("Content-Type", "application/json")
        oReq.send(JSON.stringify(body));
    } else {
        oReq.send();
    }
}

// fetch mustache template string from DOM tree, render and insert into dom tree (#content)
function render(templatename, data) {
    var output = Mustache.render(document.getElementById(templatename).innerHTML, data);
    document.querySelector("#content").innerHTML=output;
}

// shortcut for rendering errors
function render_error(data) {
    render('error', data);
}

// fetch a list of files and display it
function list_files() {
    ajax("GET", base_url+'/files', {}, function (data) {
        render('file_list', data);
    }, render_error);
}

// read a particular file and display it
function read_and_render_file(file_url, template) {
    ajax("GET", file_url, {}, function (data) { render(template, data); }, render_error);
}

// event handler for all clicks on #content
// this is mainly used because it can fetch events for elements that are not yet present
// when the event listener is created
function click_content(event) {

    var dataset = event.target.dataset;

    if (dataset['readfile']) {
        read_and_render_file(dataset['readfile'], 'file_read');
    }
    if (dataset['editfile']) {
        read_and_render_file(dataset['editfile'], 'file_edit');
    }
    if (dataset['createfile']) {
        render('file_create', {});
    }
    if (dataset['deletefile']) {
        ajax("DELETE", dataset['deletefile'], {}, function (data) {  // success
            list_files();
            document.querySelector("#message").innerHTML = "<p>Die Datei wurde erfolgreich gelöscht.</p>";
        }, function () {  // error
            document.querySelector("#message").innerHTML = data['error'];
        });
    }
}

function submit_content(event) {
    event.preventDefault();

    if (event.target.id == 'logindata') {  // the login form
        // 1. Save username/password to global variable
        // 2. Try to list files (i.e. return to initial view)
        theCredentials = { 'username': document.querySelector("#user_name").value,
                           'password': document.querySelector("#user_password").value };
        list_files();
        return;
    }

    // File edit or create form was submitted
    var id=null;
    var content=document.querySelector("#file_content").value;
    if (event.target.id == 'edit') {
        id = document.querySelector("#file_id").value;
    } else if (event.target.id == 'create') {
        id = document.querySelector("#file_name").value
    }
    if (id && id.match(/[0-9A-Za-z]+/)) {
        ajax("PUT", base_url + '/files/' + id, {id: id, content:content}, function () {
            list_files();
            document.querySelector("#message").innerHTML = "<p>Die Datei wurde erfolgreich geändert.</p>";
        }, function (status, data) {
            document.querySelector("#message").innerHTML = "<p>Fehler: "+data+"</p>";
        });
    } else {
        ajax("POST", base_url + '/files', {id: id, content:content}, function () {
            list_files();
            document.querySelector("#message").innerHTML = "<p>Die Datei wurde erfolgreich angelegt.</p>";
        }, function () {
            document.querySelector("#message").innerHTML = "<p>Fehler: "+data+"</p>";
        });
    }
}

var base_url='http://localhost:8080';
var theCredentials = null;

window.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#nav_list").addEventListener("click", list_files);
    document.querySelector('#content').addEventListener("click", click_content, true); // true: use capture phase!
    document.querySelector('#content').addEventListener("submit", submit_content, true); // true: use capture phase!
    list_files();
});

