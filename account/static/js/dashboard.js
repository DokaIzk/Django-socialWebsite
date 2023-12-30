let page = 1;
let last_page = false;
let block_request = false;

window.addEventListener('scroll', (e) => {
    let margin = document.body.clientHeight - window.innerHeight - 150;

    if (window.scrollY > margin && !last_page && !block_request) {
        block_request = true;
        page += 1;

        fetch()
    }
})
