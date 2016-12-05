
var data = [
    { title: "Client oder Server? Welcher Webdev-Typ bist du?",
      categories: ["client","server"],
      result: {
          server: "Server! <br> Klarer Fall, du magst es groß und schnell und brauchst die volle Kontrolle über alles. Dein Sternzeichen: Firewall.",
          client: "Client! <br> Du bist eher der schnieke Typ, der eine Stunde mit der Haarsträhne kämpft, obwohl der Kamm krumme Zinken hat. Dein Sternzeichen: border-radius.",
          default: "Du kannst dich nicht entscheiden. <br> Entweder bist du ein Allrounder, oder läufst vor allen Schwierigkeiten weg. Dein Sternzeichen: Middleware."
      },
      questions: [
          { question: "Was ist das Gegenteil von Tag?",
            answers: [
                { answer: "Nacht", server: 1, client: 0 },
                { answer: "/Tag", server: 0, client: 1 },
                { answer: "Was ist Tag? Scheint da diese 'Sonne'?", server: 0, client:0},
                { answer: "Attribut", server:0, client: 1}
            ]
          },
          { question: "Wenn dein Programm keine Ausgabe liefert,...",
            answers: [
                { answer: "tippst du nochmal 'RUN' ein.", server: 0, client:0},
                { answer: "drückst du Strg-C.", server: 1, client: 0 },
                { answer: "drückst du F12.", server: 0, client: 1 }
            ]
          },
          { question: "Size matters",
            answers: [
                { answer: "Du wachst oft schweißgebadet auf, weil du von einem überflüssigen Byte geträumt hast.", server: 0, client: 2 },
                { answer: "Du kennst jedes Kilobyte deines Programms mit Namen.", server: 0, client: 1 },
                { answer: "Ein Gigabyte mehr oder weniger, was macht das schon?", server: 1, client:0}
            ]
          },
          { question: "Der Nutzer...",
            answers: [
                { answer: "ist ein fernes, unbekanntes Wesen.", server: 2, client: 0 },
                { answer: "spinnt. Grundsätzlich.", server: 1, client: 1 },
                { answer: "soll gefälligst meinen Browser nehmen.", server: 0, client:1}
            ]
          },
          { question: "Elegante Programmiersprachen",
            answers: [
                { answer: "Brauch ich nicht, ich hab PHP.", server: 1, client: 0 },
                { answer: "Am liebsten schnitze ich Haskell-Code in schneeweiße Dateien.", server: 1, client: 0 },
                { answer: "Eleganz liegt im Auge des <code>(function(){Betrachters;}())();</code>", server: 0, client:1}
            ]
          }
      ]
    },

    { title: "Linux, Mac oder Windows? Welches Betriebssystem passt wirklich zu dir?",
      categories: ["linux", "mac", "windows"],
      result: {
          server: "Server! <br> Klarer Fall, du magst es groß und schnell und brauchst die volle Kontrolle über alles. Dein Sternzeichen: Firewall.",
          client: "Client! <br> Du bist eher der schnieke Typ, der eine Stunde mit der Haarsträhne kämpft, obwohl der Kamm krumme Zinken hat. Dein Sternzeichen: border-radius.",
          default: "Du kannst dich nicht entscheiden. <br> Entweder bist du ein Allrounder, oder läufst vor allen Schwierigkeiten weg. Dein Sternzeichen: Middleware."
      },
      questions: [
          { question: "Wie viele Tasten braucht eine Maus?",
            answers: [
                { answer: "Eine reicht. Völlig.", mac:2 },
                { answer: "Zwei. Ich habe schließlich auch zwei Arme.", mac:1, windows:1},
                { answer: "Unter drei geht gar nichts.", linux:1 },
                { answer: "Maus? Wozu Maus?", linux:2}
            ]
          },
          { question: "Wozu war dein letztes selbstgeschriebenes Shellskript?",
            answers: [
                { answer: "Dashboard ein- und ausschalten", mac: 1},
                { answer: "Überwachung des Ressourcenverbrauchs von Prozessen für einen Cron-Job ", linux: 1},
                { answer: "Shellskript? Nee, ich tanke bei Aral.", windows: 1 }
            ]
          },
          { question: "Für gute Software",
            answers: [
                { answer: "Zahle ich auch gerne ein bisschen mehr.", mac: 1, windows: 1 },
                { answer: "Installiere ich gerne einige dutzend Pakete und Compiler.", linux:1 },
                { answer: "Muss ich gar nichts zahlen - gibt's alles frei und kostenlos.", linux:1}
            ]
          }
      ]
    }

];

var test;  // the current test
var question;  // the current question
var score={};  // the current scores

function display_result() {
  var max_score = Number.NEGATIVE_INFINITY;
  var max_cats = [];
  html = "<p class='explanation'> &middot; ";
  for (var prop in score) {
      if (score.hasOwnProperty(prop)) {
          html += prop + " = " + score[prop] + " Punkte &middot; ";
          if (score[prop] == max_score) {
              max_cats[max_cats.length] = prop
          }
          if (score[prop] > max_score) {
              max_cats = [prop]
              max_score = score[prop]
          }
      }
  }
  html += "</ul>";
  if (max_cats.length > 1) {
      // more than one top category, take default
      max_cats=['default']
  }
  html = "<p class='result'>"+data[test]['result'][max_cats[0]]+"</p>"+html;
  document.getElementById("psychot").innerHTML = html;
};

function answer(event) {
    var answernr = event.target.dataset.answer;
    if (answernr !== undefined) {
        var q = data[test]['questions'][question];
        var a = q['answers'][answernr];
        for (var i=0; i<data[test]['categories'].length; i++) {
            var cat = data[test]['categories'][i];
            if (a[cat]) {
                score[cat] += a[cat];
            }
        }
    }
    question += 1;
    if (question >= data[test]['questions'].length) {
        display_result();
    } else {
        display_question();
    }
};

function display_question() {
    q = data[test]['questions'][question];
    html = "<header>"+data[test]['title']+"</header>"+
           "<article><header>Frage "+(question+1)+": "+q['question']+"</header><ul>";
    for (var i=0; i<q['answers'].length; i++) {
        html += "<li data-answer='"+i+"'>"+q['answers'][i]['answer']+"</li>"
    }
    html += "</ul></article>";
    document.getElementById("psychot").innerHTML = html;
    document.getElementById("psychot").addEventListener("click", answer);
};

function start_test(testnr) {
    test = testnr;
    for (var i=0; i<data[test]['categories'].length; i++) {
        score[data[test]['categories'][i]]=0;
    }
    question = 0;
    display_question();
};

function init_testlist() {
    var html ="<ul>";
    for (var i=0; i<data.length; i++) {
        html += "<li data-starttest='"+i+"'>"+data[i]["title"].split("?")[0]+"?</li>";
    }
    html += "</ul>";
    document.getElementById("testlist").innerHTML=html;
    var items = document.querySelectorAll("li[data-starttest]");
    for (i=0; i<items.length; i++) {
        items[i].addEventListener( "click", function (event) { start_test(event.target.dataset.starttest); });
    }
}

window.addEventListener("DOMContentLoaded", function () {
    init_testlist();
    start_test(0);
});