/* 
 * Tic Tac Toe in Javascript
 * 
 * Web-Technologien 2013, Blatt 3, Musterlösung
 * 
 * Tobias Thelen
 * 
 * minimax and score algorithm from https://github.com/lukasvermeer/minimax/blob/master/index.html
 *
 * 
 */

// the ttt object holds all data and methods for the game
// 

var OFF_BOARD = 3;
var WIN_SCORE = 1000;
var COL_FULL = -1;

var scoreCache = new Array();

/*
 * Field
 * 
 * The Connect 4 model.
 */
function Field(turn, field) {

    // internal field representation as 7 columns
    // columns are represented from bottom to top
	if (field != undefined) {
		this.field = field;
	} else {
		this.field = [[0,0,0,0,0,0],
		         	  [0,0,0,0,0,0],
		        	  [0,0,0,0,0,0],
		        	  [0,0,0,0,0,0],
		        	  [0,0,0,0,0,0],
		        	  [0,0,0,0,0,0],
		        	  [0,0,0,0,0,0]];
	}

	if (turn != undefined) {
		this.turn=turn;
	} else {
		this.turn = 1; // which player makes next move?
	}
}

/* 
 * f(int col, int row)
 * 
 * Getter method for field cells.
 * 
 * Returns:
 * 	0: cell is free
 *	1: cell is taken by player 1 (human player)
 * 	2: cell is taken by player 2 (computer)
 * 	OFF_BOARD: col and/or row out of bounds

 */
Field.prototype.f = function (col, row) {
	if (col < 0 || col > 6 || row < 0 || row > 5)
		return OFF_BOARD;
	else {
		//console.dir(this.field);
		return this.field[col][row];
	}
}

Field.prototype.clone = function () {
	return new Field(this.turn, [this.field[0].slice(0),
	                             this.field[1].slice(0),
	                             this.field[2].slice(0),
	                             this.field[3].slice(0),
	                             this.field[4].slice(0),
	                             this.field[5].slice(0),
	                             this.field[6].slice(0)]);
}

Field.prototype.getHash = function() { return this.field.toString(); }

Field.prototype.move = function (col) {
	// make player move
	// return COL_FULL if column is full
	for (var row=0;row<6; row++) {
		if (this.f(col,row)==0) {
			this.field[col][row]=this.turn;
			this.turn = (this.turn == 1 ? 2 : 1);
			return row;
		}
	}
	return COL_FULL;
};	

Field.prototype.remis = function () {
	// remis: no more moves possible
	// check: all columns in row 5 are taken
		for (var col=0; col < 7; col++) {
			if (this.f(col,5)===0) return false;
		}
		return true;	
}

Field.prototype.score = function (player) {
		if (scoreCache[''+player+this.getHash()]!=null)
			return scoreCache[player.toString() + this.getHash()];
			
		var score = 0;
		for (i = 0; i < 7; ++i) {
			for (j = 0; j < 7 - 4 + 1; ++j) {
				var line = new Array(6);
				for (k = 0; k < 6; ++k) { line[k]=[0,0,0,0]; }

				for (n = j; n < j + 4; ++n) {
					line[0][this.f(n,i)]++; // columns
					line[1][this.f(i,n)]++; // rows
					line[2][this.f(n,n-i)]++; // diagonal southwest half
					line[3][this.f(7-n-1,n-i)]++; // diagonal northwest half
					if (i>0) {
						line[4][this.f(n-i,n)]++; // diagonal northweast half
						line[5][this.f(n+i,7-n-1)]++; // diagonal southeast half
					}
				}

				for (k = 0; k < 6; ++k) {
					if (line[k][player]==4) return WIN_SCORE; // win
					if (line[k][(player === 1 ? 2 : 1)]==4) return -WIN_SCORE; // lose
					if (line[k][(player === 1 ? 2 : 1)]==0 && line[k][OFF_BOARD]==0) { 
						score += Math.pow(line[k][player],2); 
					}
				}
			}
		}
		scoreCache[player.toString() + this.getHash()] = score;
		return score;
}
	
function minimax(player, field, d) {
//		function minMax(p, b, d) {
// p: player designation
// b: current board state
// d: iteration depth

	var score = field.score(player);
	
	// some game states do not require any thinking (e.g. already lost or won)
	if (d == 0) return [null,score]; // max depth reached. just return the score.
	if (score == -WIN_SCORE) return [null,score]; // we lose, not good.
	if (score == WIN_SCORE) return [null,score]; // we win, good.
	if (field.remis()) return [null,8888]; // board is full, pretty good, but not as good as winning.

	// simple optimization attempt. look ahead two moves to see if win or lose possible.
	// this prevents the algorithm from exploring parts of the state space that are unrealistic to occur.
	if (d > 2) {
		for (var q = 0; q < 7; ++q) { // for each possible move.
			var n = field.clone(); // copy current state.
			if (n.move(q) !== COL_FULL) { // make move.
				var qs = minimax(player, n, 2); // look ahead one move.
				if (qs[1] == WIN_SCORE || qs[1] == -WIN_SCORE) {
					return [q,qs[1]]; // if I win or lose, stop exploring.
				}
			}
		}
	}

	// algorithm considers best and worst possible moves in one loop to save lines of code.
	var maxv = 0; // best score.
	var maxc = -1; // column where best score occurs.
	var minv = 999999; // worst score.
	var minc = -1; // colum where worst score occurs.
	for (var q = 0; q < 7; ++q) { // for each possible move.
		var n = field.clone(); // copy current state.
		if (n.move(q) !== COL_FULL) { // make move.
			var next = minimax(player, n, d-1); // look ahead d-1 moves.
			if (maxc == -1 || next[1] > maxv) { maxc = q; maxv = next[1]; } // compare to previous best.
			if (minc == -1 || next[1] < minv) { minc = q; minv = next[1]; } // compare to previous worst.
		}
	}

	if (field.turn==player) { // if it is our turn.
		return [maxc,maxv/2+score/2]; // make best possible move.
	} else { // otherwise.
		return [minc,minv/2+score/2]; // make worst possible move.
	}
}

Field.prototype.dump = function () {
	console.log("Connect 4 - Turn: "+this.turn);
	for (var row=5; row>=0; row--) {
		row_str = "";
		for (var col=0; col<7; col++) {
			row_str += this.field[col][row]+" ";				
		}
		console.log(row_str);
	}
}


var connect4 = {

	// initialize board:
	// - register click events for columns
	// - initialize field
	// - randomly determine who starts
	init: function () {
		for (var i=0; i<7; i++) {
			document.getElementById("drop-"+i).addEventListener( "click", clickdrop, false);
			for (var j=0; j<6; j++) {
				document.getElementById("field-"+i+"-"+j).addEventListener("click",clickdrop,false);
			}	
		}
		this.field=new Field();
		this.field.turn=Math.floor((Math.random()+0.5)*2); // random start
		this.set_indicator();
		if (this.field.turn == 2) {
			// computer starts
			window.setTimeout(mydrop, 500);
		}
	},
	
	// make player move
	// return false if column is full
	move: function (col) {
		row = this.field.move(col);
		this.set_indicator();
		if (row!=COL_FULL) {
			document.getElementById("field-" + col + "-" + row).classList.remove("white");
			document.getElementById("field-" + col + "-" + row).classList.add((this.field.turn === 1) ? "x" : "o");
			return true;			
		} else {
			return false;
		}
	},
	
	// make a computer move
	mymove: function () {
		var row = minimax(2, this.field, 4)[0];
		return this.move(row);
	},

	// set turn indicator according to current turn
	set_indicator: function() {
		var indicator="Du bist am Zug...";
		if (this.field.turn===2) {
			indicator="Ich bin am Zug...";
		}
		document.getElementById("indicator").innerHTML=indicator;
	}	
}

// click event handler for columns (player move)
function clickdrop() {
	var col = parseInt(this.getAttribute("data-col"));
	if (connect4.move(col)) {
		if (connect4.field.score(1) == WIN_SCORE) {
			alert("Glückwunsch! Du hast gewonnen!");
			window.location.reload();
		}
		
		if (connect4.field.remis()) {
			alert("Unentschieden.");
			window.location.reload();
		}
		
		// begin to think about move after 0.5 seconds
		window.setTimeout(mydrop, 500);
	}
}

// timeout event for computer move
function mydrop() {	
		connect4.mymove();
		if (connect4.field.score(2) == WIN_SCORE) {
			alert("Oh je! Ich habe gewonnen!");
			window.location.reload();
		}
		if (connect4.field.remis()) {
			alert("Unentschieden.");
			window.location.reload();
		}
}

// click event for start button
function start() {
	// hide start button
	document.getElementById("start").style.display="none";
	// initialize board and register click events for board columns
	connect4.init();
}


// register click handler for start button
document.addEventListener("DOMContentLoaded", function () {
	document.getElementById("start").addEventListener("click",start,false);
});

