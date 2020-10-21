let toit = "<variable_toit>"
let bp_open = document.getElementById("bp_open")
let bp_close = document.getElementById("bp_close")

// Si le toit est fermé 
if (toit == "close" ) {
  bp_close.className += 'hidden'; // Cacher FERMER   
}
// Si le toit est ouvert 
if (toit == "open" ) {
bp_open.className += 'hidden'; // Cacher FERMER   
}
