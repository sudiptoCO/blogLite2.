<template>
  <div>
    <NavBar />
    <div>
      <h2>My Followings</h2>
      <div class="following-list">
        <div v-for="(following, index) in followings" :key="index">
          <div>{{ following.name }}</div>
          <button @click="unfollow(following.id)">Unfollow</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      followings: [],
    };
  },
  methods: {
    getFollowings() {
      // make API request to get followings data @app.route('/get_followings')
      fetch('http://localhost:5001/get_followings')
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.followings = data.followings;
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
          console.log(data);
          // remove the unfollowed user from the followings array
          const index = this.followings.findIndex(following => following.id === userId);
          if (index !== -1) {
            this.followings.splice(index, 1);
          }
        })
        .catch(error => console.error(error));
    },
  },
  mounted() {
    this.getFollowings();
  },
};
</script>

<style scoped>
.following-list {
  display: flex;
  flex-direction: column;
}

.following-list > div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.following-list > div button {
  padding: 0.5rem 1rem;
  border-radius: 10px;
  background-color: #eee;
  border: none;
  outline: none;
  cursor: pointer;
}

.following-list > div button:hover {
  background-color: #ccc;
}
</style>
