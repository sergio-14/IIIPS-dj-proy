//* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}



/*asdffffffffffffffffffffffffffffffffffff*/ 
// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

const temaOscuro = () => {
  document.querySelector("main").setAttribute("data-bs-theme", "dark");
  document.querySelector("#dl-icon").setAttribute("class", "bi bi-sun-fill");
}

//Función para filtrar las categorías de los paralelos
function verCategoria(cat){
  const items = document.getElementsByClassName("item");
  for(let i=0; i < items.length;i++){
      items[i].style.display = "none";
  }

  const itemCat = document.getElementsByClassName(cat);
  for(let i = 0; i<itemCat.length;i++){
      itemCat[i].style.display = "block";
  }

  const links = document.querySelectorAll(".trabajos nav a");
  links[0].className = "";
  links[1].className = "";
  links[2].className = "";
  links[3].className = "";

  const itemSeleccionado = document.getElementById(cat);
  itemSeleccionado.className = "borde";
}

//eliminar alert //
function ConfirmDelete()
{
  var respuesta = confirm("¿Esta seguro que desea eliminar el campo?");

  if (respuesta == true)
  {
    return true;
  }
  else
  {
    return false;

  }
}