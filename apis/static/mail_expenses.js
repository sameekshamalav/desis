document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch mail expenses and update the table
    function fetchAndDisplayMailExpenses() {
        fetch('/api/mail_expenses') // Replace this URL with your API endpoint
            .then(response => response.json())
            .then(data => {
                const tableBody = document.querySelector('#expenses-table tbody');
                tableBody.innerHTML = ''; // Clear previous data

                data.forEach(expense => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${expense.date_of_purchase}</td>
                        <td>${expense.order_id}</td>
                        <td>${expense.platform}</td> 
                        <td>${expense.item}</td>
                        <td>${expense.category}</td>
                        <td>${expense.amount}</td>
                        <td>${expense.status}</td>
                        <td>${expense.feedback}</td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error fetching mail expenses:', error));
    }

    // Fetch and display mail expenses initially
    fetchAndDisplayMailExpenses();

    // Set up WebSocket connection for real-time updates
    const socket = new WebSocket('ws://localhost:8000/ws/mail_expenses/'); // Replace with your WebSocket URL

    socket.onmessage = function(event) {
        const newExpense = JSON.parse(event.data);
        const tableBody = document.querySelector('#expenses-table tbody');

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${newExpense.date_of_purchase}</td>
            <td>${newExpense.order_id}</td>
            <td>${newExpense.platform}</td> 
            <td>${newExpense.item}</td>
            <td>${newExpense.category}</td>
            <td>${newExpense.amount}</td>
            <td>${newExpense.status}</td>
            <td>${newExpense.feedback}</td>
        `;

        tableBody.insertBefore(row, tableBody.firstChild);
    };
});
