/**
 * Created by Tobias on 08.12.2016.
 */


// load list of persons and place it in the left column
function load_personlist() {
    load("#thelist", "/ajax/persons");
}

// register event handlers
window.addEventListener("DOMContentLoaded", function () {
    load_personlist();

    // load data of a person
    on("[data-personid]", "click", function (event) {
        load("#theperson", "/ajax/person/"+event.target.dataset['personid']);
    });

    // display form for adding person
    on("#new_person_button", "click", function (event) {
        load("#theperson", "/ajax/person/new/form");
    });

    // add a hobby while filling in new person form
    on("#new_person_add_hobby", "click", function (event) {
        var new_hobby=document.querySelector("#new_person_addhobby").value;
        if (new_hobby) {
            document.querySelector("#new_person_hobbylist").innerHTML +=
                "<li>"+new_hobby+"<input type='hidden' name='hobby' value='"+new_hobby+"'></li>";
        }
    });

    // add a team while filling in new person form
    on("#new_person_add_team", "click", function (event) {
        var e = document.querySelector("#new_person_team");
        var new_teamid = e.value;
        var new_team = e.options[e.selectedIndex].text;
        if (new_teamid) {
            document.querySelector("#new_person_teamlist").innerHTML +=
                "<li>"+new_team+"<input type='hidden' name='team' value='"+new_teamid+"'></li>";
        }
    });

    // submit new person form // TODO: client side validation!
    on("#new_person", "submit", function (event) {
        var data = formqs("#new_person");
        event.preventDefault();
        ajax("/ajax/person/new", function () {
            load_personlist();
            document.querySelector("#theperson").innerHTML="OK. Person angelegt.";
        }, function (oReq) {
            document.querySelector("#error").innerHTML = oReq.responseText;
        }, data);
    });

    // add a hobby to an existing person
    on("#person_add_hobby", "click", function (event) {
        var new_hobby=document.querySelector("#person_addhobby").value;
        if (new_hobby) {
            var personid = document.querySelector("#personname").dataset['pid'];
            ajax("/ajax/person/addhobby/"+personid+"/"+encodeURIComponent(new_hobby), function () {
                load("#theperson", "/ajax/person/"+personid);
            })
        }
    });

    // add a team to an existing person
    on("#person_add_team", "click", function (event) {
        var e = document.querySelector("#person_addteam");
        var teamid = e.value;
        var team = e.options[e.selectedIndex].text;
        if (teamid) {
            var personid = document.querySelector("#personname").dataset['pid'];
            ajax("/ajax/person/addteam/"+personid+"/"+teamid, function () {
                load("#theperson", "/ajax/person/"+personid);
            })
        }
    });

    // delete a person
    on("[data-deletepersonid]", "click", function (event) {
        ajax("/ajax/person/delete/" + event.target.dataset['deletepersonid'], function () {
            document.querySelector("#theperson").innerHTML = "OK. Person gelöscht.";
            load_personlist();
        });
    });

    // delete a hobby
    on("[data-deletehobby]", "click", function (event) {
        // for click on elements with attributes:
        //   data-deletehobby = "Name of the hobby" # TODO: pass hobby ids instead of names, needs changes to model code
        //   data-deletehobbypersonid = "ID of the person"
        var personid = event.target.dataset['deletehobbypersonid'];
        var hobby = encodeURIComponent(event.target.dataset['deletehobby']);
        ajax("/ajax/person/deletehobby/"+personid+"/"+hobby, function () {
            load("#theperson", "/ajax/person/"+personid);
        })
    });

    // delete a person from a team
    on("[data-deletepersonteam]", "click", function (event) {
        // for click on elements with attributes:
        //   data-deletehobby = "Name of the hobby" # TODO: pass hobby ids instead of names, needs changes to model code
        //   data-deletehobbypersonid = "ID of the person"
        var personid = document.querySelector("#personname").dataset['pid'];
        var team = encodeURIComponent(event.target.dataset['deletepersonteam']);
        ajax("/ajax/person/deleteteam/"+personid+"/"+team, function () {
            load("#theperson", "/ajax/person/"+personid);
        })
    });

});





