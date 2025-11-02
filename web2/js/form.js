function isvalidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email); //overi, zda email odpovída zadanemu regex

}
function isvalidName(name) {

}
const form = document.querySelector('.message form');
form.addEventListener('submit', function (e) {
    e.preventDefault(); //zabrání standardnímu odeslání formuláře

    const name = document.querySelector('.input__name').value.trim();
    const email = document.querySelector('.input__email').value.trim();
    const subject = document.querySelector('.input__subject').value.trim();
    const message = document.querySelector('.input__textarea').value.trim();
    if (!name || !email || !subject || !message) {
        alert("Prosím, vyplňte všechna pole.");
        return;
    }
    if (!isvalidEmail(email)) {
        alert("Zadejte email ve tvaru example@email.cz");
        return;
    }
    console.log('zobrazuji name: ' + name);
    sendMessage({ name, email, subject, message });
});

function sendMessage(data) {
    console.log("Zpráva byla odeslána:", data);
    alert("Děkujeme " + data.name + ", zpráva byla odeslána!");
}
function sendToServer(data) {
    fetch('/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: data.name,
            email: data.email,
            subject: data.subject,
            message: data.message // data formuláře převedená na JSON řetězec
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log('Server resposne:', data);
            alert("Děkujeme, zpráva byla odeslána!");
            form.reset(); //vyčistí formulář
        })
        .catch(err => {
            console.error('Chyba při odesílání:', err);
            alert('Něco se pokazilo, zkuste to znovu.')
        })

}
