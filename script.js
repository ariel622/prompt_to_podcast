function generateScript() {
    const subject = document.getElementById('subjectInput').value;
    const apiUrl = 'http://www.prompt2podcast.ariel.com/'; // Replace with your actual API URL

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ subject: subject })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('scriptOutput').innerText = data.script;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('scriptOutput').innerText = 'Failed to retrieve script.';
    });
}
