function updateImage(type)
{
    var preview = document.querySelector('img');
    var file = document.querySelector('input[type=file]').files[0];
    var b64 = document.querySelector('input.base64')
    if (type == 'entityImage')
    { 
        preview = document.querySelector('div.entity img.image');
        file = document.querySelector('input[type=file]#entityImage').files[0];
        b64 = document.querySelector('input.base64#entityImage')
    }
    else if (type == 'entityIcon')
    {
        preview = document.querySelector('div.entity img.icon');
        file = document.querySelector('input[type=file]#entityIcon').files[0];
        b64 = document.querySelector('input.base64#entityIcon')
    }
    else if (type == 'mapImage')
    {
        preview = document.querySelector('div.map img.image');
        file = document.querySelector('input[type=file]#mapImage').files[0];
        b64 = document.querySelector('input.base64#mapImage')
    }

    const reader = new FileReader();

    reader.addEventListener("load", function () {
      // convert image file to base64 string
      preview.src = reader.result;
      b64.value = reader.result;
    }, false);

    if (file) {
      reader.readAsDataURL(file);
    }
}

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
    }
    btn_ent.onclick = function() {
        modal.style.display = "block";
        modal.getElementsByClassName("entity")[0].style.display = "block";
    }
    btn_map.onclick = function() {
        modal.style.display = "block";
        modal.getElementsByClassName("map")[0].style.display = "block";
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