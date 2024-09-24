document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("control-ports-form");
    const actionSelect = document.getElementById("action");
    const messageBox = document.getElementById("message-box");

    
    function showMessage(message, type) {
        messageBox.innerText = message;
        messageBox.className = type; // Aquí puedes definir estilos para "error" e "info"
        setTimeout(() => {
            messageBox.innerText = "";
            messageBox.className = "";
        }, 5000); // Mensaje desaparece después de 5 segundos
    }
});
