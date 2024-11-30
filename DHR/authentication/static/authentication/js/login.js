document.querySelector('#login-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission
    
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    
    console.log("JavaScript working");
    console.log("Username: ", username);
    console.log("Password: ", password);
    // console.log('Access Token', data.access)

    // Disable the button to avoid multiple requests
    // document.querySelector('.login-btn').disabled = true;
    
    fetch('http://127.0.0.1:8000/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => {
        if (!response.ok) {  // Check if the response has a non-2xx status code
            return response.json().then(data => {
                // Show the error message from the server response
                alert(data.error || 'Login failed');  // If error is present in response, show it
                // throw new Error(`Login failed with status ${response.status}`);
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.access) {
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);
            if (data.user_type == 'superuser'){
                window.location.href = '/dashboard/';
            }
            else{
                if (data.election_mode == true){
                    window.location.href = '/check_voter/'
                }
                else{
                    window.location.href = '/view_all_voters/'
                    console.log(data)
                }
            }  
        } else {
            alert('Login failed: ' + (data.message || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error during login:', error);
        alert('Login failed: ' + error.message);
    });
});
