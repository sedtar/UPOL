function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email); // checks if the email matches the given regex
}

function isValidName(name) {
    // function body not implemented yet
}

const form = document.querySelector('.message form');
form.addEventListener('submit', function (e) {
    e.preventDefault(); // prevents the default form submission

    const name = document.querySelector('.input__name').value.trim();
    const email = document.querySelector('.input__email').value.trim();
    const subject = document.querySelector('.input__subject').value.trim();
    const message = document.querySelector('.input__textarea').value.trim();

    if (!name || !email || !subject || !message) {
        alert("Please fill in all fields.");
        return;
    }

    if (!isValidEmail(email)) {
        alert("Please enter an email in the format example@email.com");
        return;
    }

    console.log('Displaying name: ' + name);
    sendMessage({ name, email, subject, message });
});

function sendMessage(data) {
    console.log("Message has been sent:", data);
    alert("Thank you " + data.name + ", your message has been sent!");
}

function sendToServer(data) {
    fetch('/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: data.name,
            email: data.email,
            subject: data.subject,
            message: data.message // form data converted to a JSON string
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log('Server response:', data);
            alert("Thank you, your message has been sent!");
            form.reset(); // clears the form
        })
        .catch(err => {
            console.error('Error sending message:', err);
            alert('Something went wrong, please try again.');
        });
}
