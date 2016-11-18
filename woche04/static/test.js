/*
 * Mehrzeiliger Kommentar
 */

var empty = {};

var rascal = {
    "given-name": "Borrah",
    surname: "Minnevitch",
    name: function () { return this["given-name"]+" "+this.surname; }
}

console.log(rascal.surname);
console.log(rascal["given-name"]);
console.log(rascal.name());

var anotherRascal=Object.create(rascal);
console.log(anotherRascal.name());

rascal.prototype.age = function () {
    return 12;
}

console.log(rascal.age());
console.log(anotherRascal.age());
