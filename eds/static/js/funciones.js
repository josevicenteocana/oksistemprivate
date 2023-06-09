(function () {

    const btnEliminar = document.querySelectorAll(".btnconfirmar")

    btnEliminar.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Esta seguro de continuar?');
            if (!confirmacion) {
                e.preventDefault();
            }

        });

    });

})();