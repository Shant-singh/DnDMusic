function selectChange () {
    var current = document.querySelector('select').value;
    if (current==0)
    {
        document.querySelector('div.map').style.display = 'none';        
        document.querySelector('div.entity').style.display = 'block';
    }
    else
    {
        document.querySelector('div.entity').style.display = 'none';
        document.querySelector('div.map').style.display = 'block';        
    }
}

window.onload = function(){
    // Get the modal
    var modal = document.getElementById("modal");

    // Get the button that opens the modal
    var btn = document.getElementById("add_instance");

    // Hide each of the different modals
    selectChange();

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal
    btn.onclick = function() {
        modal.style.display = "block";
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