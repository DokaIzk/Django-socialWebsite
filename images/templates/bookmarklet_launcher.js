(() => {
    if (!window.bookmarklet) {
        let bookmarklet_js = document.body.appendChild(document.createElement('script'));

        bookmarklet_js.src = '//socialWebsite.com:8000/static/js/bookmarklet.js?r=' + 
        Math.floor(Math.random()*9999999999999999);
        
        window.bookmarklet = true
    }

    else {
        bookmarkletLaunch();
    }
})(); 