<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
  
    <div class="container-fluid">
      <router-link class="navbar-brand text-style" to="/">BlogLite</router-link>

      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profile">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/create">Create</router-link>
          </li> 
          <li class="nav-item">
            <router-link class="nav-link" to="/userslist">People</router-link>
          </li> 
        </ul>

        <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <button class="btn btn-danger" @click="logout">Logout</button>
        </li>
      </ul>
      </div>
    
    </div>
  </nav>
</template>

<script>
import axios from 'axios';
export default {

  data() {
    return {
      searchQuery: '',
      searchResults: null
    }
  },
  methods: {
    search() {
      if (this.searchQuery) {
        axios.get(`http://localhost:5001/search?q=${this.searchQuery}`).then(response => {
          this.searchResults = response.data;
          console.log(this.searchResults);
          this.$router.push({ name: 'UsersList', props: { searchResults: this.searchResults } });
        }).catch(error => {
          console.log(error);
          
        });
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  },
  
}
</script>

<style>
.text-style{
  font-size: 30px !important;
  font-family: fantasy !important;
  color:mediumblue !important;
}

.navbar {
  width: 100%;
  max-width: 1200px; /* set a maximum width for the navbar */
  margin: 0 auto; /* center the navbar horizontally */
}


</style>
