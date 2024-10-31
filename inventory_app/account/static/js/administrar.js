function editarUsuario(index) {
    const usuarioContainer = document.getElementById('usuario-'+index);

    const usuario = {
        user_id: usuarioContainer.querySelector('.usuario-id').textContent,
        nombre: usuarioContainer.querySelector('.usuario-nombre').textContent,
        correo: usuarioContainer.querySelector('.usuario-correo').textContent,
        permisos: usuarioContainer.querySelector('.usuario-permisos').textContent
    }

    document.getElementById("user_id").value = usuario.user_id;
    document.getElementById("edit-nombre").value = usuario.nombre;
    document.getElementById("edit-correo").value = usuario.correo;

    if (usuario.permisos === "admin") {
        document.getElementById("edit-permisos").children[0].selected = true;
    } else {
        document.getElementById("edit-permisos").children[1].selected = true;
    }


    document.getElementById("edit-user-form").dataset.index = index;
    document.getElementById("edit-form").style.display = "block";
}


function hideEditForm() {
    document.getElementById("edit-form").style.display = "none";
}

// Función para guardar los cambios realizados en el usuario
function saveChanges() {
    const index = document.getElementById("edit-user-form").dataset.index;
    usuarios[index] = {
        nombre: document.getElementById("edit-nombre").value,
        correo: document.getElementById("edit-correo").value,
        permisos: document.getElementById("edit-permisos").value
    };

    alert("Cambios guardados correctamente");
    hideEditForm();
}

