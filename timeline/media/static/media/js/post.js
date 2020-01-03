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
        // Later when I will need to click on post image this will come handy
        this.postImage = post.querySelector('#body-image');
        
        this.post = this.postClickable(post.querySelectorAll('*'));
        
        this.events = [
            this.pressedOptions,
            this.pressedPost
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