$(function () {
  // $("#tblUsuarios").DataTable();
  // $("#tblElementosDevolutivos").DataTable();
  $("#fileFoto").on("change", validarImagen);
  $("#fileFoto").on("change", mostrarImagen);
});

function validarImagen(evt) {
  let files = evt.target.files;
  // Nombre y tamaño del archivo
  var fileName = files[0].name;
  var fileSize = files[0].size;
  let extension = fileName.split(".").pop();
  extension = extension.toLowerCase();
  if (extension !== "jpg" && extension !== "png") {
    Swal.fire(
      "Cargar Imagen",
      "La imagen debe tener una extensión JPG o PNG",
      "warning"
    );
    $("#fileFoto").val(""); //Vaciar el campo
    $("#fileFoto").focus();
  } else if (fileSize > 900000) {
    Swal.fire(
      "Cargar Imagen",
      "La imagen NO puede superar los 900K",
      "warning"
    );
    $("#fileFoto").val("");
    $("#fileFoto").focus();
  }
}

function mostrarImagen(evt) {
  const archivos = evt.target.files;
  const archivo = archivos[0];
  const url = URL.createObjectURL(archivo);

  $("#imagenUsuario").attr("src", url);
  $("#imagenProducto").attr("src", url);
}
