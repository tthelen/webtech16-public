/**
 * Created by Tobias on 08.12.2016.
 */

function load_teamlist() {
    load("#thelist", "/ajax/teams");
}

window.addEventListener("DOMContentLoaded", function () {
    load_teamlist();

    // load data of a person
    on("[data-teamid]", "click", function (event) {
        load("#theteam", "/ajax/team/"+event.target.dataset['teamid']);
    });

    // display form for adding person
    on("#new_team_button", "click", function (event) {
        load("#theteam", "/ajax/team/new/form");
    });

    // submit new team form // TODO: client side validation!
    on("#new_team", "submit", function (event) {
        var data = formqs("#new_team");
        event.preventDefault();
        ajax("/ajax/team/new", function () {
            load_teamlist();
            document.querySelector("#theteam").innerHTML="OK. Team angelegt.";
        }, function (oReq) {
            document.querySelector("#error").innerHTML = oReq.responseText;
        }, data);
    });

    // delete a person
    on("[data-deleteteamid]", "click", function (event) {
        ajax("/ajax/team/delete/" + event.target.dataset['deleteteamid'], function () {
            document.querySelector("#theteam").innerHTML = "OK. Team gelöscht.";
            load_teamlist();
            load_teamlist();
        });
    });


    // add a team while filling in new person form
    on("#new_team_add_person", "click", function (event) {
        var e = document.querySelector("#new_team_person");
        var new_personid = e.value;
        var new_person = e.options[e.selectedIndex].text;
        if (new_personid) {
            document.querySelector("#new_team_personlist").innerHTML +=
                "<li>"+new_person+"<input type='hidden' name='person' value='"+new_personid+"'></li>";
        }
    });

    // delete a person from a team
    on("[data-deleteteamperson]", "click", function (event) {
        // for click on elements with attributes:
        //   data-deletehobby = "Name of the hobby" # TODO: pass hobby ids instead of names, needs changes to model code
        //   data-deletehobbypersonid = "ID of the person"
        var teamid = document.querySelector("#teamname").dataset['tid'];
        var personid = encodeURIComponent(event.target.dataset['deleteteamperson']);
        ajax("/ajax/person/deleteteam/"+personid+"/"+teamid, function () {
            load("#theteam", "/ajax/team/"+teamid);
        })
    });

});







/*

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


*/