function registration(event) {
    event.preventDefault(); // Prevent the default form submission

    // Gather form data
    const password = document.getElementById('password').value;
    const passwordRepeat = document.getElementById('passwordRepeat').value;
    const token = localStorage.getItem('access_token');

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
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
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
                window.location.href = '/accounts';  // Redirect after success
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

const togglePassword = document.getElementById('togglePassword');
const password = document.getElementById('password');
const togglePasswordImg = document.getElementById('togglePasswordImg');

const togglePasswordRepeat = document.getElementById('togglePasswordRepeat');
const passwordRepeat = document.getElementById('passwordRepeat');
const togglePasswordRepeatImg = document.getElementById('togglePasswordRepeatImg');

const eyeViewPath = "static/img/eye-view.svg";
const eyehidePath = "static/img/eye-hide.svg";

togglePassword.addEventListener('click', (e) => {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);

    if (togglePasswordImg.src.includes(eyeViewPath)) {
        togglePasswordImg.src = eyehidePath;
    } else{
        togglePasswordImg.src = eyeViewPath;
    }

});

togglePasswordRepeat.addEventListener('click', (e) => {
    const type = passwordRepeat.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordRepeat.setAttribute('type', type);

    if (togglePasswordRepeatImg.src.includes(eyeViewPath)) {
        togglePasswordRepeatImg.src = eyehidePath;
    } else{
        togglePasswordRepeatImg.src = eyeViewPath;
    }

});