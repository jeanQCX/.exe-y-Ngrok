document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("qrForm");
    const input = document.getElementById("contenido");

    form.addEventListener("submit", function(event) {
        if (input.value.trim() === "") {
            event.preventDefault(); // Detiene el envío al servidor
            alert("Aviso: Escribe algo primero (un link o texto).");
        }
    });
});