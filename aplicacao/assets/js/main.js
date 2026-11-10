
/* =========================================================
   1. CARREGAMENTO DE COMPONENTES HTML
   ========================================================= */

// Função responsável por carregar arquivos HTML externos
// e inserir seu conteúdo dentro de um elemento da página.
//
// elementId = ID do elemento que receberá o conteúdo.
// filePath = Caminho do arquivo HTML que será carregado.

async function loadComponent(elementId, filePath) {

    // Localiza o elemento HTML pelo seu ID.
    const element = document.getElementById(elementId);

    // Se o elemento não existir na página, interrompe a função.
    if (!element) return;

    try {

        // Busca o arquivo HTML informado.
        const response = await fetch(filePath);

        // Verifica se o arquivo foi carregado corretamente.
        if (!response.ok) {
            throw new Error(`Não foi possível carregar ${filePath}`);
        }

        // Converte o conteúdo recebido em texto HTML
        // e insere esse conteúdo dentro do elemento encontrado.
        element.innerHTML = await response.text();

    } catch (error) {

        // Exibe o erro no console do navegador.
        console.error(error);

        // Limpa o elemento caso ocorra algum problema
        // durante o carregamento do componente.
        element.innerHTML = "";
    }
}


/* =========================================================
   2. INICIALIZAÇÃO DO MENU DE NAVEGAÇÃO
   ========================================================= */

// Função responsável pelo funcionamento do menu,
// principalmente na versão mobile do StormWatch.

function initializeMenu() {

    // Localiza o botão responsável por abrir e fechar o menu.
    const toggle = document.getElementById("menuToggle");

    // Localiza a área que contém os links de navegação.
    const nav = document.getElementById("navLinks");

    // Se o botão ou a navegação não existirem, interrompe a função.
    if (!toggle || !nav) return;


    // Função auxiliar para fechar o menu.
    const closeMenu = () => {

        // Remove a classe "open", escondendo o menu.
        nav.classList.remove("open");

        // Informa aos recursos de acessibilidade
        // que o menu está fechado.
        toggle.setAttribute("aria-expanded", "false");

        // Atualiza o texto acessível do botão.
        toggle.setAttribute("aria-label", "Abrir menu");

        // Retorna o símbolo do botão para o ícone de menu.
        toggle.textContent = "☰";
    };


    // Adiciona um evento de clique ao botão do menu.
    toggle.addEventListener("click", () => {

        // Alterna a classe "open".
        // Se estiver fechado, abre.
        // Se estiver aberto, fecha.
        const open = nav.classList.toggle("open");

        // Atualiza o atributo de acessibilidade
        // de acordo com o estado atual do menu.
        toggle.setAttribute("aria-expanded", String(open));

        // Altera o texto acessível do botão.
        toggle.setAttribute(
            "aria-label",
            open ? "Fechar menu" : "Abrir menu"
        );

        // Altera o símbolo exibido no botão.
        // Aberto = X
        // Fechado = ☰
        toggle.textContent = open ? "✕" : "☰";
    });


    // Percorre todos os links dentro do menu.
    // Quando um link for clicado, o menu será fechado.
    nav.querySelectorAll("a").forEach(link => {

        link.addEventListener("click", closeMenu);

    });


    // Adiciona um evento para identificar
    // quando o usuário pressiona alguma tecla.
    document.addEventListener("keydown", event => {

        // Se a tecla pressionada for Escape,
        // fecha o menu de navegação.
        if (event.key === "Escape") {
            closeMenu();
        }
    });
}


/* =========================================================
   3. IDENTIFICAÇÃO DA PÁGINA ATUAL
   ========================================================= */

// Função responsável por identificar qual página
// está aberta e destacar o link correspondente no menu.

function initializeActiveLink() {

    // Obtém o caminho da página atual.
    // Exemplo: /pages/dashboard.html
    const path = window.location.pathname;

    // Seleciona os links do menu que possuem o atributo data-nav.
    const links = document.querySelectorAll(".nav-links a[data-nav]");


    // Percorre todos os links encontrados.
    links.forEach(link => {

        // Remove a classe "active" de todos os links.
        // Isso evita que mais de uma página fique destacada.
        link.classList.remove("active");

        // Obtém o valor do atributo data-nav do link.
        const target = link.dataset.nav;


        // Verifica se o link corresponde à página atual.
        // Início = index.html
        // Metodologia = metodologia.html
        // Impacto = impacto.html
        // Dashboard = dashboard.html

        if (
            (target === "home" &&
                (path === "/" || path.endsWith("/index.html"))) ||

            (target === "metodologia" &&
                path.endsWith("/metodologia.html")) ||

            (target === "impacto" &&
                path.endsWith("/impacto.html")) ||

            (target === "dashboard" &&
                path.endsWith("/dashboard.html"))
        ) {

            // Adiciona a classe "active" ao link correspondente.
            // Essa classe permite destacar visualmente a página atual.
            link.classList.add("active");

            // Informa aos leitores de tela
            // que este link representa a página atual.
            link.setAttribute("aria-current", "page");

        } else {

            // Remove o atributo caso o link
            // não corresponda à página atual.
            link.removeAttribute("aria-current");
        }
    });
}


/* =========================================================
   4. INICIALIZAÇÃO GERAL DO SITE
   ========================================================= */

// Função responsável por coordenar o carregamento
// dos componentes e a inicialização das funcionalidades.

async function initializeSite() {

    // Carrega o cabeçalho e o rodapé simultaneamente.
    //
    // Promise.all() aguarda os dois carregamentos terminarem
    // antes de executar as próximas instruções.

    await Promise.all([

        // Carrega o arquivo header.html
        // dentro do elemento que possui ID "header".
        loadComponent("header", "/includes/header.html"),

        // Carrega o arquivo footer.html
        // dentro do elemento que possui ID "footer".
        loadComponent("footer", "/includes/footer.html")

    ]);


    // Inicializa o funcionamento do menu
    // depois que o cabeçalho foi carregado.
    initializeMenu();

    // Identifica e destaca a página atual no menu.
    initializeActiveLink();
}


/* =========================================================
   5. EVENTO DE CARREGAMENTO DO DOCUMENTO
   ========================================================= */

// Aguarda o HTML da página ser completamente interpretado.
//
// Quando o evento DOMContentLoaded acontecer,
// executa a função initializeSite().

document.addEventListener("DOMContentLoaded", initializeSite);
