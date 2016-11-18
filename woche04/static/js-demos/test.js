/*

   Blockkommentar

 */

console.log("Test!"); // Zeilenkommentare

var student1 = {
    name: "Tobias Thelen",
    matrikelnummer: "988888",
    fach: "Informatik"
};

console.log(student1);
console.log("Name: "+student1.name);
console.log("Name: "+student1['name']);

var student2 = Object.create(student1);

console.log(student2);
student2.name = "Walter Meier";
console.log("Name: "+student2.name);

for (name in student2) {
    if (student2.hasOwnProperty(name)) {
        console.log(name+" --> " + student2[name])
    }
}
