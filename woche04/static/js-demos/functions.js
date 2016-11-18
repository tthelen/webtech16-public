
function add(x, y) {
    return x+y;
};

console.log(add(8,9));

var mult = function (x,y) {
    return x*y;
}

console.log(mult(8,9));

function scope_demo() {
    var a=9, b=10;

    function bar() {
        var b=11;
        a=8;
    }
};

function concat() {
    console.log(this);
    // console.log(a+b+c+d+e+f);
};

concat("Hallo ", "Welt!");

var student1 = {
    name: "Tobias Thelen",
    matrikel: function () { console.log(this); return "423355"; }
};

console.log(student1.matrikel());


function add_value(x) {
    return function (y) {
        return x+y;
    }
}

console.log(add_value(4)(16));

var add4 = add_value(4);
console.log(add4(26));


















