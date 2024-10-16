// home.js
document.getElementById('update-content-btn').addEventListener('click', function() {
    const contentSection = document.getElementById('dynamic-content');
    contentSection.innerHTML = `
        <h2>Updated Content</h2>
        <p>The content has been updated using JavaScript!</p>
    `;
});
