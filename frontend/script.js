document.getElementById('shorten-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const url = document.getElementById('url-input').value;
    const response = await fetch('http://localhost:5000/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
    });
    const data = await response.json();
    document.getElementById('result').innerHTML = `
        <p>Shortened URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a></p>
    `;
});
