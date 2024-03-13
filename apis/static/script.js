document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const addExpenseBtn = document.getElementById('addExpenseBtn');
    const modal = document.getElementById('expenseForm');
    const closeBtn = document.querySelector('.close');
    const cancelBtn = document.querySelector('.cancel');
    const form = document.getElementById('expenseFormContent');
    const tableBody = document.getElementById('expenseTableBody');

    // Dark Mode toggle functionality
    darkModeToggle.addEventListener('change', function() {
        document.body.classList.toggle('dark-mode');
        // Optionally, you can save the user's preference for dark mode in localStorage or a cookie
        // and apply it when the page is loaded next time.
    });

    // Show modal
    addExpenseBtn.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    // Close modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Close modal on Cancel
    cancelBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Dynamically add rows to the table
    function addRow(item, amount, category, date) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item}</td>
            <td>${amount}</td>
            <td>${category}</td>
            <td>${date}</td>
            <td><button class="edit">Edit</button> <button class="delete">Delete</button></td>
        `;
        tableBody.appendChild(row);
    }

    // Dummy data
    const expenses = [
        { item: 'Groceries', amount: '$50', category: 'Food', date: '2024-03-12' },
        { item: 'Gas', amount: '$30', category: 'Transportation', date: '2024-03-11' }
    ];

    // Populate table with dummy data
    expenses.forEach(expense => {
        addRow(expense.item, expense.amount, expense.category, expense.date);
    });

    // Submit form
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const amount = document.getElementById('amount').value;
        const item = document.getElementById('item').value;
        const category = document.getElementById('category').value;
        const date = document.getElementById('date').value;
        addRow(item, amount, category, date);
        modal.style.display = 'none';
        form.reset();
    });

    // Event delegation for delete button
    tableBody.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete')) {
            e.target.parentElement.parentElement.remove();
        }
    });

});
