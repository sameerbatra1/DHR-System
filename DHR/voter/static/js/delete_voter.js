$(document).ready(function() {
    $('.delete-btn').click(function(event) {
        event.preventDefault(); // Prevent default button action
        var voterId = $(this).data('voter-id'); // Get the voter ID

        // Show confirmation alert
        var confirmDelete = confirm("Are you sure you want to delete voter ID " + voterId + "?");

        if (confirmDelete) {
            $.ajax({
                url: '/delete_voter/' + voterId + '/', // Update this URL to match your routing
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val() // Add CSRF token
                },
                success: function(response) {
                    if (response.success) {
                        alert(response.message); // Show success message
                        location.reload(); // Reload the page to see the changes
                    } else {
                        alert(response.message); // Show error message
                    }
                },
                error: function(xhr, status, error) {
                    alert("An error occurred: " + error); // Handle error
                }
            });
        }
    });
});
