window.onload = function(){
    // Get the modal
    var modal = document.getElementById("modal");

    // Get the button that opens the modal
    var btn_gam = document.getElementById("create_game");
    var btn_ent = document.getElementById("create_entity");
    var btn_map = document.getElementById("create_map");

    // Hide each of the different modals
    modal.getElementsByClassName("game")[0].style.display = "none";
    modal.getElementsByClassName("entity")[0].style.display = "none";
    modal.getElementsByClassName("map")[0].style.display = "none";

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal 
    btn_gam.onclick = function() {
        modal.style.display = "block";
        modal.getElementsByClassName("game")[0].style.display = "block";
        console.log("game");
    }
    btn_ent.onclick = function() {
        modal.style.display = "block";
        modal.getElementsByClassName("entity")[0].style.display = "block";
        console.log("entity");
    }
    btn_map.onclick = function() {
        modal.style.display = "block";
        modal.getElementsByClassName("map")[0].style.display = "block";
        console.log("map");
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
        modal_contents = modal.getElementsByClassName("modal-content")[0].getElementsByTagName("div");
        console.log(modal_contents)
        for (var i=0; i<modal_contents.length; i++)
        {
            modal_contents[i].style.display = "none";
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
};