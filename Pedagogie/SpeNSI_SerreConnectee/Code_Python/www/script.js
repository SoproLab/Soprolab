// Solution proposée : création d'un fichier javascript associé au HTML
// Le code Python de la fonction page_Web ( ...) est chargé de réaliser la page HTML envoyée au navigateur. C'est dans cette fonction que l'on remplacera <variable_toit> par l'état de la trappe
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
