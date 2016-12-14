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

function load_personlist() {
    load("#thelist", "/ajax/persons");
}

function load_person(event) {
    if (event.target.dataset['personid']) {
        load("#theperson", "/ajax/person/"+event.target.dataset['personid'])
    }
}

window.addEventListener("DOMContentLoaded", function () {
    load_personlist();
    document.querySelector("body").addEventListener("click", load_person, true);

});

