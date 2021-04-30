let ledv = "<etat_Ledv>"
let ledv_on = document.getElementById("ledv_on")
let ledv_off = document.getElementById("ledv_off")

// Si la led verte est allumée fermé 
if (ledv == "OFF" ) {
  ledv_off.className += 'hidden'; // Cacher ETEINDRE   
}
// Si la led verte est éteinte 
if (ledv == "ON" ) {
  ledv_on.className += 'hidden'; // Cacher ALLUMER
}
