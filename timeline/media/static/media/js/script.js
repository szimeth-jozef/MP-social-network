console.log("global script")

import EventSystem from './post.js';
import { makeLike, getSearchResults, addResultsToPopup } from './helperFunctions.js';

// Loaded elements
const textarea = document.getElementById('id_text');

// Uploaded image elements
const loadedImageContainer = document.getElementById('id-upld-image-container');    // This is a div which contains the image itself and it's related things <div>    
const loadedImage = document.getElementById('loaded_image');                        // The loaded image itself <img>
const clearButton = document.getElementById('id_x-button');                         // X button which is actually a div <div>

const imageInput = document.getElementById('id_image'); // Image input <input>


// Event listeners
if (textarea) {
    textarea.addEventListener('input', function(event) {
        textarea.style.height = 'inherit';
        const computed = window.getComputedStyle(textarea);
        const height = parseInt(computed.getPropertyValue('padding-top'), 10)
                        + textarea.scrollHeight;
                        // + parseInt(computed.getPropertyValue('border-top-width'), 10) 
                        // + parseInt(computed.getPropertyValue('padding-bottom'), 10)
                        // + parseInt(computed.getPropertyValue('border-bottom-width'), 10);
        
        textarea.style.height = height + 'px';
    });
}

if (clearButton) {
    clearButton.addEventListener('click', function() {
        loadedImageContainer.setAttribute('class', 'hidden_elm');
        imageInput.value = null;
    });
}

if (imageInput) {
    imageInput.addEventListener('change', function() {
        if (imageInput.files && imageInput.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                loadedImage.setAttribute('src', e.target.result);
                loadedImage.setAttribute('class', 'uploaded_img');
                loadedImageContainer.setAttribute('class', 'upld-image-container');
                clearButton.setAttribute('class', 'x-button')
            };

            reader.readAsDataURL(imageInput.files[0]);
        }
    });
}


// Load elements
const followButton = document.getElementById('followButton');
const token = document.getElementById('token');


// Event listeners
if (followButton) {
    followButton.addEventListener('click', function() {

        const url = "http://localhost:8000/site/api/makefollow/";

        const data = {
            followed: followButton.value
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token.value}`
            },
            body: JSON.stringify(data)

        })
        .then(response => response.json())
        .then(json => {
            console.log("Response:", json);
            followButton.innerText = json.buttonText;
            document.getElementById('followingCount').innerText = `${json.following} Following`; 
            document.getElementById('followerCount').innerText = `${json.followers} Followers`;
        });
    });
}



// all posts on current page
const postsOnPage = document.getElementsByClassName('post');

const es = new EventSystem(postsOnPage);


// Event listener for like buttons
for (const post of postsOnPage) {
    const button = post.getElementsByClassName('clickablepart')[0];
    const slug = post.getElementsByClassName('post-slug')[0].value;
    let state = null;
    button.addEventListener('click', function() {
        state = button.src.match(/fire-up-lit-logo\.png$/) ? true : false;

        makeLike(state, slug, token)
            .then(response => {
                if (response.state) {
                    const newSource = button.src.replace(/fire-up-none-logo\.png/, "fire-up-lit-logo.png");
                    button.src = newSource;
                } else {
                    const newSource = button.src.replace(/fire-up-lit-logo\.png/, "fire-up-none-logo.png");
                    button.src = newSource;
                }

                post.getElementsByClassName('number-of-likes')[0].innerText = response.count;
            });
    });
}


// Search popup box event handler
const searchInput = document.getElementById('search-bar');
const popup = document.getElementById('popup-box');

searchInput.addEventListener('keyup', function() {
    const keyword = searchInput.value;

    if (keyword.trim().length !== 0) {
        popup.classList.add('show-popup');
        getSearchResults(keyword)
            .then(res => addResultsToPopup(popup, res));
    } else {
        popup.innerHTML = '';
        popup.classList.remove('show-popup');
    }
});


// Edit profile change images preview
const banner_input = document.getElementById('id_banner_picture');
const profile_input = document.getElementById('id_profile_picture');

if (banner_input && profile_input) {
    const banner_image = document.getElementById('banner');
    const profile_image = document.getElementById('profile');

    banner_input.addEventListener('change', function() {
        const reader = new FileReader();
        reader.onload = function (e) {
            banner_image.setAttribute('src', e.target.result);
        };
        reader.readAsDataURL(banner_input.files[0]);
        
    });

    profile_input.addEventListener('change', function() {
        const reader = new FileReader();
        reader.onload = function (e) {
            profile_image.setAttribute('src', e.target.result);
        };
        reader.readAsDataURL(profile_input.files[0]);
        
    });
}