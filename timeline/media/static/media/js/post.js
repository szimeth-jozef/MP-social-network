import { deletePost } from './helperFunctions.js';

export default class EventSystem {
    constructor(trackable) {
        this.trackable = this.createTrack(trackable);
        this.listen();
    }

    createTrack(t) {
        const arr = [];
        for (const element of t) {
            arr.push(new Post(element));
        }
        return arr;
    }

    listen() {
        const self = this;
        document.addEventListener('click', function(event) {
            const target = event.target;
            for (const tracked of self.trackable) {

                tracked.match(target);
            }
        });
    }
}

class Post {
    constructor(post) {
        this.parent = post;

        this.optionsBtn = post.querySelector('.options-button-img');
        
        this.optionsBox = post.querySelector('.options-box');
        this.options = this.optionsBox.children;
        this.deleteOption = post.querySelector('.delete-post');
        // Later when I will need to click on post image this will come handy
        this.postImage = post.querySelector('#body-image');
        
        this.post = this.postClickable(post.querySelectorAll('*'));
        
        this.events = [
            this.pressedOptions,
            this.pressedPost,
            this.pressedDelete,
            this.pressedPostImage
        ];
    }

    pressedOptions(t) {
        if (t === this.optionsBtn || this.matchMultipleElements(t, this.options)) {
            this.optionsBox.style.display = 'block';
        }
        else if (t === this.optionsBox) {
            // console.log("Do nothing");
        } else {
            this.optionsBox.style.display = 'none';
        }
    }

    pressedPost(t) {
        const exclude = [
            this.parent.querySelector('.full-name'),
            this.parent.querySelector('.profile-on-post'),
            this.parent.querySelector('.clickablepart'),
            this.parent.querySelector('.comment-icon')
        ];

        if (!this.matchMultipleElements(t, exclude)) {
            if (this.matchMultipleElements(t, this.post) || t === this.parent) {
                const slug = this.parent.querySelector('#post-slug').value;
                window.location.href = "http://localhost:8000/site/post/" + slug + "/";
            }
        }

    }

    pressedDelete(t) {
        if (t === this.deleteOption) {
            const slug = this.parent.querySelector('#post-slug').value;
            const conf = confirm("Are you sure you want to delete this post?");

            if (conf) {
                deletePost(slug).then(res => {
                    if (res.success) {
                        // Remove the deleted post from the page
                        this.parent.parentNode.removeChild(this.parent);
                        // Get the post count number, if exists the decrement it
                        const postsCount = document.getElementById('post-count');
                        if (postsCount) {
                            let number = Number(postsCount.innerText);
                            number--;
                            postsCount.innerText = String(number);
                        }
                    } else {
                        console.error("Couldn't delete this post!");
                    }
                });
            }
        }
    }

    pressedPostImage(t) {
        if (t === this.postImage) {
            const container = document.querySelector('.post-image-viewer');
            container.style.display = 'block';
            document.body.classList.add('stop-scroll-body');

            container.querySelector('#image-view-close-button').addEventListener('click', function() {
                container.style.display = 'none';
                document.body.classList.remove('stop-scroll-body');
            });
        }
    }

    match(target) {
        for (const event of this.events) {
            event.call(this, target);
        }
    }

    postClickable(all) {
        const passed = []; 

        const exclude = [
            this.optionsBtn,
            this.optionsBox,
            this.postImage
        ];

        for (let i = 0; i < all.length; i++) {
            if (!(this.matchMultipleElements(all[i], exclude) || this.matchMultipleElements(all[i], this.options))) {
                passed.push(all[i]);
            }
        }

        return passed;
    }

    matchMultipleElements(target, elements) {
        if (!isIterable(elements)) {
            throw `${elements} is not iterable`
        }

        for (const el of elements) {
            if (el === target) {
                return true;
            }
        }
        return false;
    }
    
}

function isIterable(obj) {
    // checks for null and undefined
    if (obj == null) {
      return false;
    }
    return typeof obj[Symbol.iterator] === 'function';
  }