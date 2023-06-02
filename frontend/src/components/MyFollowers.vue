<template>
    <div>
        <NavBar />
    <div>
      <h2>My Followers</h2>
      
      <div class="follower-list">
        <div v-for="follower in followers" :key="follower.id">
          <div>{{ follower.name }}</div>
          <button v-if="follower.is_following" @click="unfollow(follower.id)">Unfollow</button>
          <button v-else @click="follow(follower.id)">Follow</button>
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
        followers: [],
      };
    },
    methods: {
      getFollowers() {
        // make API request to get followers data @app.route('/get_followers')
        fetch('http://localhost:5001/get_followers')
          .then(response => response.json())
          .then(data => {
            console.log(data)
            this.followers = data.followers.map(follower => {
              return {
                id: follower.id,
                name: follower.name,
                is_following: true
              }
            });
          })
          .catch(error => console.error(error));
      },
      follow(userId) {
  // make API request to follow the user with userId
  fetch('http://localhost:5001/follow', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      follower_id: '',
      followed_id: userId
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      // update the is_following property of the follower
      const follower = this.followers.find(f => f.id === userId);
      if (follower) {
        follower.is_following = true;
      }
    })
    .catch(error => console.error(error));
},

unfollow(userId) {
  // make API request to unfollow the user with userId
  fetch('http://localhost:5001/unfollow', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      follower_id: "",
      followed_id: userId
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      // update the is_following property of the follower
      const follower = this.followers.find(f => f.id === userId);
      if (follower) {
        follower.is_following = false;
      }
    })
    .catch(error => console.error(error));
}


,
    },
    mounted() {
      this.getFollowers();
    }
  };
  </script>
  
  <style scoped>
  .follower-list {
    display: flex;
    flex-direction: column;
  }
  .follower-list > div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 10px;
  }
  .follower-list > div button {
    padding: 0.5rem 1rem;
    border-radius: 10px;
    background-color: #eee;
    border: none;
    outline: none;
    cursor: pointer;
  }
  .follower-list > div button:hover {
    background-color: #ccc;
  }
  </style>
  