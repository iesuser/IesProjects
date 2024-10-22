function registration(event) {
    event.preventDefault(); // Prevent the default form submission

    // Gather form data
    const password = document.getElementById('password').value;
    const passwordRepeat = document.getElementById('passwordRepeat').value;

    // Check if passwords match
    if (password !== passwordRepeat) {
        showAlert('danger', 'შეყვანილი პაროლები ერთმანეთს არ ემთხვევა ერთმანეთს.');
        return;
    }
    
    // Gather form data
    const formData = {
        name: document.getElementById('name').value,
        lastname: document.getElementById('lastname').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        passwordRepeat: document.getElementById('passwordRepeat').value
    };

    // Send POST request to the registration API
    fetch('/api/registration', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        return response.json().then(data => {
            return {
                status: response.status,
                data: data
            };
        });
    })
    .then(({ status, data }) => {
        if (status === 200) {
            showAlert('success', data.message);
            setTimeout(() => {
                window.location.href = '/login';  // Redirect after success
            }, 2000);
        } else {
            showAlert('danger', data.error || 'რეგისტრაციისას მოხდა შეცდომა.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// Attach the login function to the form's submit event
document.getElementById('registrationForm').onsubmit = registration;
