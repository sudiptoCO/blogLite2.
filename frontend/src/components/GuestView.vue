<template>
    <div>
      <NavBar />
      <div class="container-fluid mt-5">
        <div class="row justify-content-center">
          <div class="col-sm-12 col-md-8 col-lg-6">
            <div class="card mx-auto">
              <div class="card-body">
                <h5 class="card-title">{{ username }}'s Profile</h5>
                <hr>
                <p class="card-text"><strong>Name:</strong> {{ name }}</p>
                <p class="card-text"><strong>Followers:</strong> {{ followers }}</p>
                <p class="card-text"><strong>Following:</strong> {{ following }}</p>
                <p class="card-text"><strong>Posts:</strong> {{ posts }}</p>
                <button v-if="!isfolld" @click="followUser" class="btn btn-primary">Follow</button>
                <button v-if="isfolld" @click="unfollowUser" class="btn btn-danger">Unfollow</button>
              </div>
            </div>
          </div>
        </div>
        <div class="container mt-5">
          <h1>{{ username }}'s Posts</h1>
          <div class="row">
            <div class="col-sm-12 col-md-6 col-lg-4 mb-4" v-for="article in articles" :key="article.id">
              <div class="post shadow-sm">
                <img :src=" article.image_base64" alt="Hello">
                <div class="post-body">
                  <h5 class="post-title">{{ article.title }}</h5>
                  <p class="post-text">{{ article.text }}</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">{{ article.timestamp }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  
  
  <script>
  import NavBar from './NavBar.vue';
  
  export default {
    components: { NavBar },
    data() {
      return {
        username: '',
        name: '',
        followers: 0,
        following: 0,
        posts: 0,
        articles: [],
      };
    },
    mounted() {
      const storedIsFollowed = localStorage.getItem('isfolld');
         if (storedIsFollowed) {
            this.isfolld = JSON.parse(storedIsFollowed); // Parse the value from string to boolean
  }

      const userId = this.$route.params.id;
      fetch(`http://localhost:5001/users/${userId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log(data)
          this.username = data.name;
          this.name = data.name;
          this.followers = data.num_followers;
          this.following = data.num_followings;
          this.posts = data.num_posts;
        })
        .catch(error => console.error(error));
        
      fetch(`http://localhost:5001/get_user_posts/${userId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
        .then((resp) => resp.json())
        .then((data) => {
          this.articles.push(...data.posts);
          console.log(data);
        })
        .catch((error) => {
          console.error(error);
        });

  fetch('http://localhost:5001/isfollowed', {
  method: 'POST', // Use POST method to send JSON data in request body
  headers: {
    'Content-Type': 'application/json' // Set content type to application/json
  },
  body: JSON.stringify({ // Convert JS object to JSON string
    "follower_id": "",
    "followed_id": this.$route.params.id
  })
})
.then(response => response.json())
.then(data => {
  // Access the follow or not follow status from the 'data' object
  const isFollowed = data.is_followed;
  this.isfolld = data.is_followed;
  localStorage.setItem('isfolld', isFollowed);
  if (isFollowed) {
    console.log('user is followed');
  } else {
    console.log('user is not followed');
  }

})
.catch(error => {
  // Handle any errors that may occur during the fetch request
  console.error('Error fetching isFollowed status:', error);
});

    
},

    methods: {
    followUser() {

  fetch('http://localhost:5001/follow', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      follower_id: '',
      followed_id: this.$route.params.id
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      // update the is_following property of the follower
      const follower = this.followers.find(f => f.id === this.$route.params.id);
      if (follower) {
        follower.is_following = true;
      }
    })
    .catch(error => console.error(error));
      
    },
    unfollowUser() {

      fetch('http://localhost:5001/unfollow', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      follower_id: "",
      followed_id: this.$route.params.id
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      // update the is_following property of the follower
      
      
    })
    .catch(error => console.error(error));

      
    }
  }


  };
  </script>
<style>
.card {
  border-radius: 10px;
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.card-title {
  font-weight: bold;
  margin-bottom: 1rem;
}

.card-text {
  margin-bottom: 1rem;
}

.text-muted {
  font-size: 0.8rem;
}

.post img {
  max-width: 100%;
  height: auto;
  object-fit: cover;
  margin-bottom: 1rem;
}

.post-body {
  margin: 0; /* remove default margin */
}

.row {
  display: flex;
  flex-wrap: wrap;}
</style>


