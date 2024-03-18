document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = 'http://localhost:8000'; // Substitua pela URL real da API
    const currentBalanceElement = document.getElementById('current-balance');
    const transactionsListElement = document.getElementById('transactions-list');
    const transactionForm = document.getElementById('transaction-form');
    const balanceInitForm = document.getElementById('balance-init-form');
    const resetBalanceButton = document.getElementById('reset-balance');
    const filterTransactionsButton = document.getElementById('filter-transactions');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');

    // Fetch current balance
    async function fetchCurrentBalance() {
        const response = await fetch(`${apiUrl}/current_balance/`);
        const balance = await response.json();
        currentBalanceElement.textContent = balance.toFixed(2);
    }

    // Add transaction
    transactionForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const amount = document.getElementById('amount').value;
        const description = document.getElementById('description').value;
        const date = document.getElementById('date').value;

        const response = await fetch(`${apiUrl}/transactions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ amount, description, date })
        });

        if (response.ok) {
            fetchCurrentBalance();
            fetchTransactions();
        }
    });

    // Initialize balance
    balanceInitForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const amount = document.getElementById('initial-amount').value;
        const date = document.getElementById('initial-date').value;

        const response = await fetch(`${apiUrl}/initialize_balance/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ amount, date })
        });

        if (response.ok) {
            fetchCurrentBalance();
            fetchTransactions();
        }
    });

    // Reset balance
    resetBalanceButton.addEventListener('click', async function() {
        const response = await fetch(`${apiUrl}/reset_balance/`, {
            method: 'POST'
        });

        if (response.ok) {
            fetchCurrentBalance();
            fetchTransactions();
        }
    });

    // Filter transactions
    filterTransactionsButton.addEventListener('click', function() {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        fetchTransactions(startDate, endDate);
    });

    // Fetch transactions
    async function fetchTransactions(startDate = '', endDate = '') {
        let url = `${apiUrl}/transactions/`;
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        if (params.toString()) url += `?${params.toString()}`;

        const response = await fetch(url);
        const transactions = await response.json();
        transactionsListElement.innerHTML = '';
        // Ordena as transações pela data
        transactions.sort((a, b) => new Date(b.date) - new Date(a.date));
        // Pega apenas as últimas 7 transações
        const lastTransactions = transactions.slice(0, 7);
        lastTransactions.forEach(transaction => {
            const listItem = document.createElement('li');
            listItem.textContent = `${transaction.date} - ${transaction.description}: ${transaction.amount}`;
            transactionsListElement.appendChild(listItem);
        });
    }

    fetchCurrentBalance();
    fetchTransactions();
});
