function login(event) {
    event.preventDefault();  // Prevent the form from submitting

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;

    // Create a JSON object with the form values
    const formData = {
        email: email,
        password: password
    };

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            // JWT ტოკენების შენახვა localStorage-ში
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            localStorage.setItem('user_email', email);

            // Redirect to /projects page
            window.location.href = '/';
        } else {
            showAlert('danger', data.error || ' გაუმართავი ავტორიზაცია.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Attach the login function to the form's submit event
document.getElementById('loginForm').onsubmit = login;
