document.getElementById('scan-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const endpoints = document.getElementById('endpoints').value.trim().split('\n');
    const scans = Array.from(document.querySelectorAll('input[name="scans"]:checked')).map(cb => cb.value);
    
    fetch('/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ endpoints: endpoints, scans: scans }),
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = data.redirect;
    })
    .catch(error => console.error('Error:', error));
});
