$(document).ready(function() {
    $('.delete-btn').click(function(event) {
        event.preventDefault(); // Prevent default button action
        const Id = $(this).data('user-id'); // Get the user ID
        const token = localStorage.getItem('access'); // Get the access token

        if (!token) {
            alert("No access token found. Please log in.");
            return;
        }

        // Show confirmation alert
        const confirmDelete = confirm("Are you sure you want to delete user " + Id + "?");

        if (confirmDelete) {
            // First, check if the user is a superuser
            fetch('http://127.0.0.1:8000/check_superuser/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to verify superuser status');
                }
                return response.json();
            })
            .then(data => {
                // Proceed to delete if the user is a superuser
                if (data.is_superuser) {
                    return fetch('http://127.0.0.1:8000/delete_user/' + Id + '/', {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    });
                } else {
                    throw new Error("Access denied: You do not have superuser privileges.");
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete user');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert(data.message); // Show success message
                    location.reload(); // Reload the page to reflect changes
                } else {
                    alert(data.message); // Show error message
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred: ' + error.message); // Handle errors
            });
        }
    });
});
