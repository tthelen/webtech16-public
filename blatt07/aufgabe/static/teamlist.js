/**
 * Created by Tobias on 08.12.2016.
 */

function load(sel, url) {
    oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function () {
        document.querySelector(sel).innerHTML = this.responseText;
    });
    oReq.open("GET", url);
    oReq.send();
}

function load_teamlist() {
    load("#thelist", "/ajax/teams");
}

function load_team(event) {
    if (event.target.dataset['teamid']) {
        load("#theteam", "/ajax/team/"+event.target.dataset['teamid'])
    }
}

window.addEventListener("DOMContentLoaded", function () {
    load_teamlist();
    document.querySelector("body").addEventListener("click", load_team, true);

});



var oReq = XMLHttpRequest();
oReq.addEventListener("load", function () { console.log(this.responseText); });
oReq.open("http://localhost:8080/ajax/team/77");
oReq.send();


