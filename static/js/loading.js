function showLoading() {
    const loadingHTML = `
        <div id="loading-overlay" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 32, 64, 0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        ">
            <div class="loading-spinner"></div>
            <p style="color: white; margin-top: 2rem; font-size: 1.125rem;">Loading...</p>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', loadingHTML);
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            showLoading();
        });
    });
    
    const links = document.querySelectorAll('a[href^="/admin"], a[href^="/student"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            showLoading();
        });
    });
});
