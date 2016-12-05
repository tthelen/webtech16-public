/**
 * Created by Tobias Thelen on 11.03.2015.
 */

/**
 * Gebe zu einem validierten Element eine Nachricht aus.
 * Die Nachricht msg wird in ein Element mit per Konvention gebildeter id
 * geschrieben (-msg anhängen), wenn ok false ist. Sonst wird eine
 * eventuell vorhandene Nachricht gelöscht.
 *
 * Beispiel-HTML:
 * <input name=celsius id=celsius data-validate=float><span id=celsius-msg></span>
 */
function msg(element, ok, msg) {
    var e = document.getElementById(element.id + "-msg");
    if (e) {
        e.innerHTML = ok ? "ok" : msg;
    }
}

function validate_int(element, match) {
    var ok = (!isNaN(parseInt(element.value, 10)));
    console.log("validate_int = "+ok);
    msg(element, ok, "Bitte eine ganze Zahl eingeben!");
    return ok;
}

function validate_float(element, match) {
    var ok = (!isNaN(parseFloat(element.value)));
    console.log("validate_float = "+ok);
    msg(element, ok, "Bitte eine Zahl eingeben!");
    return ok;
}

function validate_regex(element, match) {
    var ok = (element.value.match(new RegExp(match[1])));
    console.log("validate_regex = "+element.value+" und "+match[1]);
    msg(element, ok, "Die Eingabe ist ungültig.");
    return ok;
}

function validate(event) {
    // fetch all elements in the submitted form that have a data-validate attribute
    var inputs = event.target.querySelectorAll("[data-validate]");
    var checks = [
        [/^int$/i, validate_int],
        [/^float$/i, validate_float],
        [/^regex:\/(.*)\/$/i, validate_regex]
    ];
    var ok = true;
    for (var i = 0; i < inputs.length; i++) {
        for (var j = 0; j < checks.length; j++) {
            console.log("Prüfe "+checks[j][0]+" mit "+inputs[i].id);
            match = inputs[i].getAttribute('data-validate').match(checks[j][0]);
            if (match) {
                var check = checks[j][1](inputs[i], match);
                if (!check) {
                    ok = false;
                }
            }
        }
    }
    if (!ok) event.preventDefault();
}

function validate_init() {
    var forms = document.getElementsByTagName("form");
    for (var i = 0; i < forms.length; i++) {
        console.log("Registriere event 'submit' an form mit id="+ forms[i].id);
        forms[i].addEventListener('submit', validate);
    }
}

window.onload = function () {
    validate_init();
}
