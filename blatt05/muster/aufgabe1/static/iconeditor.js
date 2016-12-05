/**
 * Created by Tobias on 14.05.2015.
 *
 * Musterlösung Blatt 3
 *
 * Erweitern Sie den Icon-Editor aus der Vorlesung (vorlesung-03.zip im Dateibereich) um folgende Funktionen:

    1. Invertieren: Führen Sie eine Schaltfläche ein, die das Bild invertiert
       (bei jeder Zelle/Pixel jeden einzeln der RGB-Werte auf 255-Wert setzen) [5 Punkte]
    2. Schwarz/Weiß-Pinsel: Führen Sie einen zusätzlichen "Pinsel" ein, der eine Zelle/Pixel schwarz färbt,
       wenn sie nicht schwarz ist, ansonsten weiß [5 Punkte]
    3. Pinselbreite: Führen Sie die Eigenschaft "Pinselbreite" ein, die regelt, wie groß die gesetzten Punkte
       (derzeit immer 1x1 Zellen/Pixel) sind. Mit einem Schieberegler (Tipp: <input type="range">) soll es möglich sein,
       für die Pinselbreite einen Wert zwischen 1 und 10 einzustellen, der dann dergestalt berücksichtigt wird, dass
       ein Klick anschließend n x n Zellen/Pixel große Punkte erzeugt, wobei der Klickpunkt links oben im entstehenden
       Quadrat ist. [5 Punkte]
    4. Icons laden: Es soll rein clientseitig möglich sein, eines der unter "vorhandene Icons" angezeigten
       Icons per Klick in den Editor zu übernehmen, um es zu bearbeiten und unter gleichem oder neuem Namen zu
       speichern. (Sie müssen dazu ein Image-Objekt erstellen, das mit der Data-URL als Quelle versehen wird und
       nach dem laden dieser Quelle auf den Canvas-Kontext angezeigt wird. Anschließend können Sie die Pixel per
       getImageData auslesen) [5 Punkte]
 */

function create_table() {
    var tablediv=document.getElementById('icon-table');
    var table = document.createElement("table");
    table.className = "icon-table";
    tablediv.appendChild(table);
    for (var i = 0; i < 16; i++) {
        var tr = document.createElement("tr");
        table.appendChild(tr);
        for (var j = 0; j < 16; j++) {
            var td = document.createElement("td");
            td.className = "icon-pixel";
            td.id="pixel-"+ i + "-" + j;
            td.style.backgroundColor = "rgb(255,255,255)"; // no dash - css attribute name becomes camelCase
            td.addEventListener("mouseover", setpixel_if_drawing);
            td.addEventListener("click", setpixel);
            tr.appendChild(td);
        }
    }
}

/* construct the color picker table */
function create_color_picker() {
    var tablediv = document.getElementById('color-picker');
    var table = document.createElement("table"); // create table
    table.className = "color-picker-table"; // assign css class
    tablediv.appendChild(table); // hang the table into the page dom tree
    var tr;
    var count = 0;
    var step = 63; // step width for picker generation. smaller width means more colors
    for (var r=0; r < 256; r += step) {
        for (var g=0; g < 256; g += step) {
            for (var b = 0; b < 256; b += step) {
                if (count++ % 24 === 0) {  // new row
                    tr = document.createElement("tr");
                    table.appendChild(tr);
                }
                var td = document.createElement("td"); // new cell
                td.className = "picker-pixel";
                td.style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
                td.addEventListener("click", choosecolor); // register click callback
                tr.appendChild(td);
            }
        }
    }
    // register callbacks for specials brushes
    // document.getElementById("bw-switcher").addEventListener("click", choose_bw_switcher);
    // document.getElementById("random").addEventListener("click", choose_random_brush);

}

/* click callback for selection one color */
function choosecolor(event) {
    var currentColor=document.getElementById("current-color");
    currentColor.innerHTML="&nbsp;&nbsp;&nbsp;";
    currentColor.style.backgroundColor = this.style.backgroundColor;
    currentColor.removeAttribute("data-mode");
}

/* click callback for special brush 'black/white switcher' */
function choose_bw_switcher(event) {
    var currentColor=document.getElementById("current-color");
    currentColor.innerHTML = this.innerHTML;
    currentColor.style.backgroundColor = "rgb(255,255,255)";
    currentColor.setAttribute('data-mode', 'bw-switch');
}

/* click callback for special brush 'random' */
function choose_random_brush(event) {
    var currentColor=document.getElementById("current-color");
    currentColor.innerHTML = this.innerHTML; // copy special brush icon
    currentColor.style.backgroundColor = "rgb(255,255,255)"; // clear background
    currentColor.setAttribute('data-mode', 'random'); // add mode name as data attribute
}

var pixel_drawing = false;

function setpixel_draw(event) {
    pixel_drawing = true;
}

function setpixel_nodraw(event) {
    pixel_drawing = false;
}

function setpixel_if_drawing(event) {
    if (!pixel_drawing) return;
    setpixel(event);
}

/* set pixels using current brush (color, mode, width) after click */
function setpixel(event) {

    var cc = document.getElementById("current-color"); // current color element contains color or special brush information
    var mode="color"; // which kind of brush do we use?
    if (cc.hasAttribute('data-mode')) mode=cc.getAttribute('data-mode');
    var m = event.target.id.match(/pixel-([0-9]+)-([0-9]+)/i); // matchgroups m[1] and m[2] contain coordinates
    if (m) {
        var x = parseInt(m[1]); // must be explicitly converted, otherwise x+w in for loop would be concatenated string
        var y = parseInt(m[2]);
        var w = get_brushwidth();
        for (var i=x; i<16 && i<x+w; i++) { // two loops to walk around the matrix
            for (var j=y; j<16 && j<y+w; j++) {
               var pixel = document.getElementById("pixel-" + i + "-" + j);
               switch (mode) {
                   case 'bw-switch':
                       // set pixel to black if not black, set to white otherwise
                       var col = pixel.style.backgroundColor;
                       pixel.style.backgroundColor = (col == "rgb(0, 0, 0)") ? "rgb(255, 255, 255)" : "rgb(0, 0, 0)";
                       break;
                   case 'random':
                       // set pixel to a random rgb value
                       // rc is helper function that return a random number x | 0 <= x < 256
                       var rc = function () { return Math.floor(Math.random()*256); }
                       pixel.style.backgroundColor = "rgb(" + rc() + "," + rc() + "," + rc() + ")";
                       break;
                   case 'color':
                   default:
                       // set pixel to currently selected color
                       pixel.style.backgroundColor = cc.style.backgroundColor;
                       break;
               }
            }
        }
    }
    preview(); // update preview
}

/* create a preview image on a canvas */
function preview() {
    var canvas = document.getElementById('preview-canvas');
    var ctx = canvas.getContext("2d");
    for (var i=0; i<16; i++) {
        for (var j=0; j<16; j++) {
            ctx.fillStyle = document.getElementById("pixel-"+i+"-"+j).style.backgroundColor;
            ctx.fillRect(j,i,1,1);
        }
    }
    document.getElementById("save-icon").value = canvas.toDataURL();
}

/* invert entire icon */
function invert(event) {
    for (var i=0; i<16; i++) {
        for (var j=0; j<16; j++) {
            var cell=document.querySelector("#pixel-"+i+"-"+j);
            // extract rgb values from css color representation by regex match
            var m = cell.style.backgroundColor.match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
            if( m) {
                // invert = set each color value to its difference from 255
                cell.style.backgroundColor = "rgb("+(255-m[1])+","+(255-m[2])+","+(255-m[3])+")";
            }
        }
    }
    preview(); // show the changed icon
}

/* set all pixels to current chosen color (or white if special brush is selected) */
function clear(event) {
    for (var i=0; i<16; i++) {
        for (var j=0; j<16; j++) {
            var cell=document.querySelector("#pixel-"+i+"-"+j);
            cell.style.backgroundColor = document.getElementById("current-color").style.backgroundColor;
        }
    }

    preview(); // show the changed icon
}

/* display value of range-input element as number */
function display_brushwidth(event) {
    document.querySelector("#brush-width-display").innerHTML = get_brushwidth();
}

/* return value of range-input element for setting the brush width */
function get_brushwidth() {
    return parseInt(document.querySelector("#brush-width").value);
}

/* load an icon from server generated icon list to preview canvas and pixel editor */
function load_icon(event) {

    // we need to do two steps:
    // 1. draw the image object to the canvas
    // 2. loop the canvas pixels and set pixel editor background colors

    var canvas = document.getElementById('preview-canvas');
    var ctx = canvas.getContext("2d");

    ctx.drawImage(event.target, 0, 0); // "event.target" is an Image object that can be drawn to the canvas
    for (var i=0; i<16; i++) { // loop through all the pixels
        for (var j=0; j<16; j++) {
            // getImageData returns a flat list with rgba (a=alpha) values
            // so rgba holds [r,g,b,a]
            var rgba = ctx.getImageData(j, i, 1, 1).data;
            // set backgroundColor property in editor table
            document.getElementById("pixel-"+i+"-"+j).style.backgroundColor = "rgb("+rgba[0]+","+rgba[1]+","+rgba[2]+")";
        }
    }
}

/* add a click callback to every icon in server generated list of saved icons */
function register_iconlist_callback() {
    var icons = document.querySelectorAll("footer .icon-list-item img");
    for (var i=0; i<icons.length; i++) {
        icons[i].addEventListener("click", load_icon);
    }
}


window.onload = function () {
    validate_init(); // prepare form validation
    create_table(); // construct large pixel table
    create_color_picker(); // construct color picker and special brushes
    window.addEventListener("mousedown",setpixel_draw, true);
    window.addEventListener("mouseup", setpixel_nodraw, true);
    // document.querySelector("#invert").addEventListener("click", invert); // register callback for invert command
    // document.querySelector("#clear").addEventListener("click", clear); // register callback for invert command
    document.querySelector("#brush-width").addEventListener("input", display_brushwidth); // register callback for range input for brush width
    register_iconlist_callback(); // make icons from server clickable
    display_brushwidth(); // show the current brush width
    preview(); // construct and show a preview image
}

