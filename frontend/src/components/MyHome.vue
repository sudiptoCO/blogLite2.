<template>
  <div class="container mt-6">
    <NavBar />
    <div v-for="post in posts" :key="post.post_id" class="card mb-3">
      <div class="card-body">
        <em><h5 class="card-title font-italic clr-text" @click="goToGuestView(post.author_id)">{{ post.name }}</h5></em>
        <h5 class="card-title">{{ post.post_title }}</h5>
        <div class="mb-3">
          <img :src="post.image64" class="card-img-top" :alt="`Image for ${post.post_title}`">
        </div>
        <p class="card-text">{{ post.post_text }}</p>
        <p class="card-text"><small class="text-muted">{{ post.timestamp }}</small></p>
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
      posts: [],
    };
  },

  methods: {
    async getFeed() {
      try {
        const token = localStorage.getItem('token');

        const response = await fetch('http://127.0.0.1:5001/get_feed', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
        });

        if (!response.ok) {
          throw new Error(response.statusText);
        }

        const data = await response.json();

        
        this.posts = [];

        
        for (const authorId in data) {
          for (const post of data[authorId]) {
            this.posts.push(post);
          }
        }
      } catch (error) {
        console.error(error);
      }
    },
    goToGuestView(id) {
      this.$router.push({ path: `/guestview/${id}` });
    }
    
  },

  created() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.$router.push('/login');
    } else {
      this.getFeed();
    }
  },
};
</script>

<style>
.card-img-top {
  height: 600px;
  object-fit: contain;
  max-width: 100%;
}

.card-title {
  font-family: cursive;
}

.card-text {
  font-family: Arial, sans-serif;
}
.clr-text {
  color: rgb(51, 153, 255)
}

</style>
