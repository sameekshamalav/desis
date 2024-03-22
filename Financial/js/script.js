const expensebtn= document.getElementById('submitExpense');
expensebtn.addEventListener('click', function() {
    // Collect form data
    const formData = new FormData(document.getElementById('addExpenseForm'));

    // Make a POST request using Fetch API
    fetch('http://127.0.0.1:8000/add', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Clear form fields
            document.getElementById('item').value = '';
            document.getElementById('amount').value = '';
            document.getElementById('category').selectedIndex = 0;
            document.getElementById('date').value = '';

            // Display success message
            document.getElementById('message').innerHTML = '<div class="alert alert-success" role="alert">Expense added successfully!</div>';
        } else {
            // Display error message
            document.getElementById('message').innerHTML = '<div class="alert alert-danger" role="alert">Failed to add expense. Please try again.</div>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById("yesButton").addEventListener("click", function() {
    window.open("http://127.0.0.1:8000/comparepredict", "_blank");
    hideConfirmation();
});

document.getElementById("noButton").addEventListener("click", function() {
    hideConfirmation();
});

function hideConfirmation() {
    document.getElementById("confirmationMessage").style.display = "none";
    document.getElementById("yesButton").style.display = "none";
    document.getElementById("noButton").style.display = "none";
}