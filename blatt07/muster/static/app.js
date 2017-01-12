
// replace the content of a dom element with html loaded via xhr GET request
function load(sel, url) {
    oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function () {
        document.querySelector(sel).innerHTML = this.responseText;
    });
    oReq.open("GET", url);
    oReq.send();
}

// make an xmlhttprequest to url
// url: url to send request to
// callback: function to be called if status==200
// callback_error: function to be called otherwise
// data: if data is absent or empty, a GET request will be issued
//       if data is given (www-form-urlencoded assumed!), a POST request will issued
function ajax(url, callback, callback_error, data) {
    oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function () {
        if (oReq.status == 200) {
            callback && callback(oReq);  // success handler (pass xhr object)
        } else {
            callback_error && callback_error(oReq);  // error handler (pass xhr object)
        }
    });
    if (!data) {
        oReq.open("GET", url);
        oReq.send();
    } else {
        oReq.open("POST", url);
        oReq.send(data);
    }
}

// get FormData for form and format it as www-form-urlencoded
function formqs(formsel) {
    var data = new FormData(document.forms[0]);
    var qs="";
    var first=true;
    for (var pair of data.entries()) {
        if (!first) qs+="&"; else first=false;
       qs+=pair[0]+"="+ encodeURIComponent(pair[1]);
    }
    return qs;
}

// wrap event handlers for elements that are not present yet
// sel: string CSS Selector for elements for which the handler should be called
// type: string Event type ("click", "mouseover", ...)
// callback: function Callback to be called. Event parameter will be passed.
function on(sel, type, callback) {
    document.addEventListener(type, function (event) {
        if (event.target.matches(sel)) {  // Element.matches is true if element would be selected by queryselector sel
            event.stopPropagation();
            callback(event);
        }
    }, true);
}
