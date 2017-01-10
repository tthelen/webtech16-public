
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
function ajax(method, url, body, successhandler, errorhandler) {
    oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function () {
        var data = JSON.parse(oReq.responseText);
        if (oReq.status==200) {
            successhandler && successhandler(data); // call successhandler if given
        } else {
            errorhandler && errorhandler(oReq.status, data);
        }
    });
    oReq.open(method, url);
    if (method == 'POST' || method == 'PUT') {
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
function read_file(file_url) {
    ajax("GET", file_url, {}, function (data) { render('file_read', data); }, render_error);
}

// event handler for all clicks on #content
// this is mainly used because it can fetch events for elements that are not yet present
// when the event listener is created
function click_content(event) {
    if (event.target.dataset['readfile']) {
        read_file(event.target.dataset['readfile']);
    }
}

var base_url='http://localhost:8080';

window.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#nav_list").addEventListener("click", list_files);
    document.querySelector('#content').addEventListener("click", click_content, true); // true: use capture phase!
    list_files();
});

