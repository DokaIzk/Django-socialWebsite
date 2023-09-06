const siteUrl = '//socialWebsite.com:8000/';
const styleURL = `${siteUrl}static/css/bookmarklet.css`;
const minWidth = 250;
const minHeight = 250;

// Load CSS
let head = document.getElementsByTagName('head')[0];
let link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleURL + '?r=' + Math.floor(Math.random() * 9999999999999999);
head.appendChild(link);

// Load HTML
let body = document.getElementsByTagName("body")[0];
let boxHtml = ` 
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a>
        <h1>Select An Image To Bookmark:</h1>
        <div class="images"></div>
    </div> `;


body.innerHTML += boxHtml;

const bookmarkletLaunch = () => {
    let bookmarklet = document.getElementById("bookmarklet");
    let imagesFound = bookmarklet.querySelector(".images");
    let closeMenu = bookmarklet.querySelector("#close");

    // clear images
    imagesFound.innerHTML = "";

    // display bookmarklet
    bookmarklet.style.display = "block";

    // close bookmarklet
    closeMenu.addEventListener('click', () => bookmarklet.style.display = 'none')


    // find imaeges with the minimun dimensions
    let images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');

    images.forEach(image => {
        if (image.naturalHeight >= minHeight && image.naturalWidth >= minWidth) {
            let imageFound = document.createElement('img');
            imageFound.src = image.src;
            imagesFound.append(imageFound);
        }
    });

    // select an image event
    imagesFound.querySelectorAll('img').forEach(image => {
        image.addEventListener('click', (event) => {
            imageSelected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteUrl + 'images/create-image/?url=' + encodeURIComponent(imageSelected.src) + '&title=' + encodeURIComponent(document.title), '_blank');
        });
    });
};

bookmarkletLaunch();
