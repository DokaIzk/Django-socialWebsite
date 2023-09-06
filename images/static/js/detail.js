const url = "{% url 'images:liked' %}";

    let options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    }

    let likeButton = document.querySelector('a.like');

    if (likeButton) {
        likeButton.addEventListener('click', (e) => {
            e.preventDefault();
    
            let formData = new FormData();
            formData.append('id', likeButton.dataset.id);
            formData.append('action', likeButton.dataset.action);
            options['body'] = formData;

            fetch(url, options)
            .then(response => response.json())
            .then(data => {
                if (data['status'] === 'ok') {
                    let previousAction = likeButton.dataset.action;

                    let action = previousAction === 'like' ? 'unlike' : 'like';
                    likeButton.dataset.action = action;
                    likeButton.innerHTML = action;

                    let likeCount = document.querySelector('.count .total');
                    let totalLikes = parseInt(likeCount.innerHTML);

                    likeCount.innerHTML = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1; 
                }
            })
        });

    }