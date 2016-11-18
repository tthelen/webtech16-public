/**
 * Created by Tobias on 14.05.2015.
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
            td.addEventListener("click", setpixel)
            tr.appendChild(td);
        }
    }
}

function create_color_picker() {
    var tablediv = document.getElementById('color-picker');
    var table = document.createElement("table");
    table.className = "color-picker-table";
    tablediv.appendChild(table);
    var tr;
    var count = 0;
    var step = 63;
    for (var r=0; r < 256; r += step) {
        for (var g=0; g < 256; g += step) {
            for (var b = 0; b < 256; b += step) {
                if (count++ % 24 === 0) {  // new row
                    tr = document.createElement("tr");
                    table.appendChild(tr);
                }
                var td = document.createElement("td");
                td.className = "picker-pixel";
                td.style.backgroundColor = "rgb("+r+","+g+","+b+")";
                td.addEventListener("click", choosecolor);
                tr.appendChild(td);
            }
        }
    }
}

function choosecolor(event) {
    var currentColor=document.getElementById("current-color");
    currentColor.style.backgroundColor = this.style.backgroundColor;
}

function setpixel(event) {
    var currentColor=document.getElementById("current-color").style.backgroundColor;
    this.style.backgroundColor = currentColor;
    preview();
}

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


window.addEventListener("DOMContentLoaded", function () {
    validate_init();  // fieser Hack!
    create_table();
    create_color_picker();
    preview();
});

