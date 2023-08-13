// // Agregar evento de clic al botón "Agregar al carrito"
// document.querySelectorAll('.producto-agregar').forEach(item => {
//   item.addEventListener('click', event => {
//     // Obtener información del producto
//     let producto = event.target.closest('.box');
//     let nombreProducto = producto.querySelector('.card-title').textContent;
//     let precioProducto = producto.querySelector('.woocommerce-Price-amount').textContent;
//     let imagenProducto = producto.querySelector('.card-img-top').src;

//     // Agregar producto al carrito
//     agregarProductoAlCarrito(nombreProducto, precioProducto, imagenProducto);
//   })
// })

// // Función para agregar producto al carrito
// function agregarProductoAlCarrito(nombre, precio, imagen) {
//   // Crear fila para el producto en la tabla del carrito
//   let fila = document.createElement('tr');
//   fila.innerHTML = `
//     <td><img src="${imagen}" alt="${nombre}" width="50"></td>
//     <td>${nombre}</td>
//     <td>${precio}</td>
//     <td>1</td>
//     <td>
//       <button type="button" class="btn btn-warning">Editar Producto</button>
//       <button type="button" class="btn btn-danger">Eliminar</button>
//     </td>
//   `;

//   // Agregar fila a la tabla del carrito
//   document.querySelector('.table tbody').appendChild(fila);

//   // Actualizar total del carrito
//   actualizarTotalCarrito();
// }

// // Función para actualizar el total del carrito
// function actualizarTotalCarrito() {
//   let total = 0;
//   document.querySelectorAll('.table tbody tr').forEach(fila => {
//     let precio = parseFloat(fila.cells[2].textContent.replace('$', ''));
//     let cantidad = parseInt(fila.cells[3].textContent);
//     total += precio * cantidad;
//   })
//   document.querySelector('.container p').textContent = `Total: $${total}`;
// }
