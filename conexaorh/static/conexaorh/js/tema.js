// --- Funções do Modal ---
// Usaremos as versões mais completas das suas funções

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        // Adiciona um efeito de fade-in via CSS se a classe existir
        modal.style.animation = 'fadeIn 0.3s ease-out forwards';
        modal.scrollTop = 0; // Garante que o modal comece do topo
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        // Adiciona um efeito de fade-out
        modal.style.animation = 'fadeOut 0.3s ease-out forwards';
        // Espera a animação terminar para esconder o modal
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }
}


// --- Inicialização Principal (quando a página carrega) ---

document.addEventListener('DOMContentLoaded', function () {

    // --- LÓGICA DO TEMA ---
    const themeToggleBtn = document.getElementById('themeToggleBtn'); // Assumindo que o botão de tema na sua navbar tenha este ID
    if (themeToggleBtn) {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateIcon(savedTheme);

        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateIcon(newTheme);
        });

        function updateIcon(theme) {
            const icon = themeToggleBtn.querySelector('i');
            if(icon) {
                 icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }


    // --- LÓGICA DOS MODAIS (FECHAR COM ESC E CLIQUE FORA) ---
    // Fechar com a tecla 'Escape'
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            document.querySelectorAll('.modal').forEach(modal => {
                if (modal.style.display === 'block') {
                    closeModal(modal.id);
                }
            });
        }
    });

    // Fechar ao clicar no fundo
    window.onclick = function (event) {
        if (event.target.classList.contains('modal')) {
            closeModal(event.target.id);
        }
    };


    // --- INICIALIZAÇÃO DE PLUGINS (JQUERY) ---
    // Verifica se jQuery está disponível antes de usar
    if (window.jQuery) {
        
        // Função para ativar o Select2
        function ativarSelect2ComTema() {
            const selectIds = [
                '#id_beneficios', '#id_processo_seletivo', '#id_sexo',
                '#id_exige_viagem', '#id_cnh', '#id_tipo_movimentacao',
                '#id_tipo_adicional', '#id_justificativa_movimentacao',
                '#id_substituicao', '#id_tipo_desligamento', '#id_motivo_desligamento',
                '#id_tipo_aviso', '#id_substituicao2'
            ];

            selectIds.forEach(function(id) {
                const element = $(id);
                if (element.length) { // Verifica se o elemento existe na página
                    if (element.hasClass("select2-hidden-accessible")) {
                        element.select2('destroy');
                    }
                    element.select2({
                        placeholder: 'Selecione uma ou mais opções',
                        width: '100%',
                        dropdownAutoWidth: true
                    });
                }
            });
        }
        
        // Ativa o Select2 na carga inicial
        ativarSelect2ComTema();

        // Observador para re-inicializar o Select2 na troca de tema
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                    ativarSelect2ComTema();
                }
            });
        });
        observer.observe(document.documentElement, { attributes: true });


        // Inicializar DataTables
        const table = $('#tabela-movimentacoes');
        if (table.length) {
            table.DataTable({
                responsive: true,
                pageLength: 5,
                lengthMenu: [5, 10, 15, 20],
                language: {
                    url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
                },
                columnDefs: [
                    { responsivePriority: 1, targets: 1 }, 
                    { responsivePriority: 2, targets: 2 },
                ]
            });
        }
    }


    // --- LÓGICA ADICIONAL (Vanilla JS) ---

    // Pré-visualização da assinatura
    const signatureInputs = document.querySelectorAll('input[type="file"][name="assinatura_gestor_proposto"]');
    signatureInputs.forEach(input => {
        input.addEventListener('change', function() {
            const preview = this.closest('form').querySelector('.signature-preview');
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

});