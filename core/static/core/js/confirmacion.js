
function confirmarEliminacion(id){
	
	Swal.fire({
		title: '¿Estás seguro?',
		text: "no podras deshacer esto!",
		icon: 'warning',
		showCancelButton: true,
		confirmButtonColor: '#3085d6',
		cancelButtonColor: '#d33',
		confirmButtonText: 'Si, eliminar',
		cancelButtonText: 'Cancelar',
	  }).then((result) => {
  		//if (result.value) {
  		if (result.isConfirmed) {
  		// redirigir
  			window.location.href = "/eliminar-pelicula/"+id+"/";
  		}
	  })
}