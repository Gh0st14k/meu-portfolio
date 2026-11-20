
// Aguarda o carregamento do HTML
document.addEventListener("DOMContentLoaded", function () {

    // Seleciona todos os links do menu
    const links = document.querySelectorAll(".nav-links a");

    // Percorre cada link
    links.forEach(function (link) {

        // Adiciona um evento de clique
        link.addEventListener("click", function () {

            console.log("Navegação realizada:", link.textContent);

        });

    });

    // Mensagem no console
    console.log("Portfólio carregado com sucesso!");

});
