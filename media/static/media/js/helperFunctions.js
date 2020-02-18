const baseURL = 'http://litfire.herokuapp.com/site/api/';

export async function makeLike(state, slug, token) {
    const likeURL = baseURL + 'like/';

    const data = {
        state: state,
        slug: slug
    };
    
    const response = await fetch(likeURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token.value}`
        },
        body: JSON.stringify(data)
    });

    return await response.json();
}

export async function getSearchResults(keyword) {
    const url = baseURL + `${keyword}/`;

    const response = await fetch(url);

    return await response.json();
}

export async function deletePost(slug) {
    const url = baseURL + `delete/${slug}/`;

    const response = await fetch(url, { method:'DELETE' });
    
    return await response.json();
}

export function addResultsToPopup(box, res) {
    box.innerHTML = '';

    for (const user of res.users) {
        const name = document.createElement('p');
        const nameHolder = document.createElement('div');
        name.innerText = user.fullName;
        nameHolder.setAttribute('class', 'popup-result');
        nameHolder.appendChild(name);

        nameHolder.addEventListener('click', function() {
            window.location.href = 'http://litfire.herokuapp.com/site/' + `${user.username}/`;
        });

        // nameHolder.classList.add('div-debug');

        box.appendChild(nameHolder);
    }
}

export async function createComment(text, slug, token) {
    const commentURL = baseURL + 'createComment/';

    const data = {
        text: text,
        slug: slug
    };

    const response = await fetch(commentURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token.value}`
        },
        body: JSON.stringify(data)
    });
    return response;
}