// Fetch and display data in the table
async function fetchAccounts() {
    const token = localStorage.getItem('access_token');
    try {
        const response = await fetch('/api/accounts', {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Authorization': `Bearer ${token}`,  // Add your JWT token here
            }
        });

        if (!response.ok) throw new Error('Failed to fetch data');

        const data = await response.json();
        populateTable(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

function populateTable(accounts) {
    const tbody = document.getElementById('accountsTableBody');
    tbody.innerHTML = ''; // Clear existing data

    accounts.forEach(account => {
        const {id, username, email, role } = account;
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>
                <strong>${username}</strong> <br>
                <span style="font-size: x-small;">${email}</span>
            </td>
            <td>
                ${role.name}
                <button class="btn btn-sm btn-outline-primary ms-2" style="font-size: x-small;" onclick="changeRole(${id})">
                    Chng Role
                </button>
            </td>
            <td>${role.is_admin ? 'Yes' : 'No'}</td>
            <td>${role.can_users ? 'Yes' : 'No'}</td>
            <td>${role.can_project ? 'Yes' : 'No'}</td>
            <td>${role.can_geophysic ? 'Yes' : 'No'}</td>
            <td>${role.can_geologic ? 'Yes' : 'No'}</td>
            <td>${role.can_hazard ? 'Yes' : 'No'}</td>
            <td>${role.can_geodetic ? 'Yes' : 'No'}</td>
            <td><button class="btn btn-info btn-sm">Edit Role</button></td>
        `;
        tbody.appendChild(row);
    });
}

// Fetch the data when the page loads
document.addEventListener('DOMContentLoaded', fetchAccounts);
