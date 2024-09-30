document.addEventListener('DOMContentLoaded', () => {
    const changePasswordCheck = document.getElementById('changePasswordCheck');
    const passwordFields = document.getElementById('passwordFields');
    const newPasswordFields = document.getElementById('newPasswordFields');

    // Toggle password fields based on checkbox state
    changePasswordCheck.addEventListener('change', () => {
        if (changePasswordCheck.checked) {
            passwordFields.style.display = 'block';
            newPasswordFields.style.display = 'block';

            // Make password fields required
            document.getElementById('user_old_password').setAttribute('required', true);
            document.getElementById('user_new_password').setAttribute('required', true);
            document.getElementById('user_repeat_new_password').setAttribute('required', true);

        } else {
            passwordFields.style.display = 'none';
            newPasswordFields.style.display = 'none';

            // Remove required attribute
            document.getElementById('user_old_password').removeAttribute('required');
            document.getElementById('user_new_password').removeAttribute('required');
            document.getElementById('user_repeat_new_password').removeAttribute('required');
        }
    });
});

// Open the modal for editing a User record
function openUserModal() {
    const token = localStorage.getItem('access_token');
    const emailText = document.getElementById('user_email');
    const roleText = document.getElementById('user_role');
    fetch(`/api/account`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,  // Include the JWT token
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 401) {
                showAlert('danger', 'სესიის ვადა ამოიწურა. გთხოვთ, თავიდან შეხვიდეთ სისტემაში.');
                clearSessionData();
            } else if (response.status === 403) {
                showAlert('danger', 'არ გაქვთ უფლებები ამ მონაცემების ნახვისთვის.');
            } else {
                showAlert('danger', 'მოხდა შეცდომა მონაცემების გამოთხოვისას.');
            }
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            document.getElementById('userUUID').value = data.uuid;
            document.getElementById('user_name').value = data.name;
            document.getElementById('user_lastname').value = data.lastname;
            emailText.textContent = data.email;
            roleText.textContent = data.role_name;
        } else {
            showAlert('danger', 'მომხმარებელი არ მოიძებნა.');
        }
    })
    .catch(error => console.error('Error fetching data:', error));


    const modal = new bootstrap.Modal(document.getElementById('UserModal'));
    modal.show();
}

function submitUserForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('UserForm'));
    const UUIDField = document.getElementById('userUUID').value;
    const changePasswordCheck = document.getElementById('changePasswordCheck').checked;
    const roleName = document.getElementById('user_role').textContent;

    formData.append('change_password', changePasswordCheck);
    formData.append('role_name', roleName);

    const token = localStorage.getItem('access_token');

    // makeApiRequest is in the globalAccessControl.js
    makeApiRequest(`/api/account/${UUIDField}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    })
    .then(data => {
        if (data.error) {
            closeModal('UserModal')
            showAlert('danger', data.error || ' გაუმართავი პროფილის რედაქტირება.');
        } else {
            window.location.reload(); // Reload the page to reflect changes
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}