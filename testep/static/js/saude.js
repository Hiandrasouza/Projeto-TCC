// Função para mostrar/ocultar campos com base no valor selecionado no dropdown "Doente e Gestante"
document.addEventListener('DOMContentLoaded', () => {
    const doenteSelect = document.getElementById('doente');
    const intercorrenciaGroup = document.getElementById('intercorrencia-group');
    const gestanteSelect = document.getElementById('gestante');
    const gestanteFields = document.getElementById('gestante-fields');

    // Função para mostrar/ocultar campos "Doente"
    function toggleDoenteFields() {
        const isSick = doenteSelect.value === 'sim';
        intercorrenciaGroup.style.display = isSick ? 'block' : 'none';
    }

    // Função para mostrar/ocultar campos "Gestante"
    function toggleGestanteFields() {
        const isGestante = gestanteSelect.value === 'sim';
        gestanteFields.style.display = isGestante ? 'block' : 'none';
    }

    // Adiciona eventos 'change' para verificar quando a seleção muda
    doenteSelect.addEventListener('change', toggleDoenteFields);
    gestanteSelect.addEventListener('change', toggleGestanteFields);

    // Executa as funções inicialmente para garantir que os campos estejam corretos ao carregar a página
    toggleDoenteFields();
    toggleGestanteFields();
});

document.addEventListener("DOMContentLoaded", function() {
    let currentMonth = new Date().getMonth();
    let currentYear = new Date().getFullYear();
    const monthYearDisplay = document.getElementById("month-year");
    const calendarBody = document.getElementById("calendar-body");
    const modal = document.getElementById("task-modal");
    const closeModal = document.getElementsByClassName("close")[0];
    const addTaskBtn = document.getElementById("add-task-btn");
    const taskDateInput = document.getElementById("task-date");
    let selectedCell = null; // Para rastrear o dia selecionado



    // Função para renderizar o calendário
    function renderCalendar(month, year) {
        calendarBody.innerHTML = ""; // Limpa o corpo do calendário
        const firstDay = new Date(year, month).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        let date = 1;
        
        for (let i = 0; i < 6; i++) {
            let row = document.createElement("tr");
            for (let j = 0; j < 7; j++) {
                if (i === 0 && j < firstDay) {
                    let cell = document.createElement("td");
                    row.appendChild(cell);
                } else if (date > daysInMonth) {
                    break;
                } else {
                    let cell = document.createElement("td");
                    cell.textContent = date;

                    // Adiciona evento de clique para selecionar o dia
                    cell.addEventListener("click", function() {
                        const selectedDate = new Date(year, month, date).toLocaleDateString('pt-BR');
                        taskDateInput.value = selectedDate;

                        // Remove a classe 'selected' da célula anterior
                        if (selectedCell) {
                            selectedCell.classList.remove("selected");
                        }

                        // Adiciona a classe 'selected' à célula clicada
                        cell.classList.add("selected");
                        selectedCell = cell; // Atualiza o dia selecionado
                    });

                    row.appendChild(cell);
                    date++;
                }
            }
            calendarBody.appendChild(row);
        }

        // Atualiza o cabeçalho do mês/ano
        const options = { month: 'long', year: 'numeric' };
        const formattedDate = new Date(year, month).toLocaleDateString('pt-BR', options);
        monthYearDisplay.textContent = formattedDate.charAt(0).toUpperCase() + formattedDate.slice(1);
    }

    // Navegar para o mês anterior
    document.getElementById("prev-month").addEventListener("click", function() {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar(currentMonth, currentYear);
    });

    // Navegar para o próximo mês
    document.getElementById("next-month").addEventListener("click", function() {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar(currentMonth, currentYear);
    });

    // Exibe o modal ao clicar no botão "Adicionar Tarefa"
    addTaskBtn.addEventListener("click", function() {
        modal.style.display = "flex";
    });

    // Fecha o modal ao clicar no X
    closeModal.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Fecha o modal ao clicar fora da área de conteúdo
    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // Inicializa o calendário com o mês e ano atual
    renderCalendar(currentMonth, currentYear);
});
