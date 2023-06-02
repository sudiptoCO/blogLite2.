<template>
  <div>
    <NavBar />
    <div class="container">
      <h1 class="my-4">People</h1>
      
      <form @submit.prevent="handleSubmit" class="my-4">
        <div class="input-group">
          <input type="text" class="form-control" v-model="searchTerm" placeholder="Search for users">
          <button type="submit" class="btn btn-primary">Search</button>
        </div>
      </form>
      
      <ul v-if="searchResults && searchResults.users.length" class="list-group">
        <li v-for="user in searchResults.users" :key="user.id" class="list-group-item" @click="goToGuestView(user.id)">
          <div class="d-flex justify-content-between align-items-center">
            <h3>{{ user.name }}</h3>
           
          </div>
          <div>
            <span class="badge bg-secondary">{{ user.num_followers }} followers</span>
            <span class="badge bg-secondary">{{ user.num_followings }} following</span>
            <span class="badge bg-primary rounded-pill">{{ user.num_posts }} posts</span>
          </div>
        </li>
      </ul>
    
      <p v-else>No users found.</p>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue';
export default {
  components: { NavBar },
  data() {
    return {
      searchTerm: '',
      searchResults: null,
    };
  },
  methods: {
    handleSubmit() {
      fetch(`http://localhost:5001/search?q=${this.searchTerm}`)
        .then(response => response.json())
        .then(data => {
          this.searchResults = data;
          console.log(this.searchResults);
        })
        .catch(error => console.error(error));
    },
    goToGuestView(id) {
      this.$router.push({ path: `/guestview/${id}` });
    },
  },
};
</script>

