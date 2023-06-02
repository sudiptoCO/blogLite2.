<template>
  <div>
    <NavBar />
    <div class="container-fluid mt-5">
      <div class="row justify-content-center">
        <div class="col-sm-12 col-md-8 col-lg-6">
          <div class="card mx-auto">
            <div class="card-body">
              <h5 class="card-title">Profile</h5>
              <hr>
              <p class="card-text"><strong>Name:</strong> {{ name }}</p>
              <p class="card-text"><strong>Followers:</strong> <router-link to="/myfollowers">{{ followers }}</router-link></p>
              <p class="card-text"><strong>Following:</strong> <router-link to="/myfollowings">{{ following }}</router-link></p>
              <p class="card-text"><strong>Posts:</strong> {{ posts }}</p>
              <button class="btn btn-primary" @click="exportData">Export Data</button>
            </div>
          </div>
        </div>
      </div>
      <div class="container mt-5">
        <h1>My Posts</h1>
        <div class="row">
          <div class="col-sm-12 col-md-6 col-lg-4 mb-4" v-for="article in articles" :key="article.id">
            <div class="post shadow-sm">
              <img :src=" article.image_base64" alt="Hello">
              <div class="post-body">
                <h5 class="post-title">{{ article.title }}</h5>
                <p class="post-text">{{ article.text }}</p>
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">{{ article.timestamp }}</small>
                  <div class="btn-group">
                    <button type="button" class="btn btn-sm btn-outline-primary" @click="editPost(article)">Edit</button>
                    <button type="button" class="btn btn-sm btn-outline-danger" @click="deletePost(article)">Delete</button>
                  </div>
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
      name: '',
      followers: 0,
      following: 0,
      posts: 0,
      articles: [],
    };
  },
  mounted() {
    fetch('http://localhost:5001/getmyinfo', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        this.name = data.name;
        this.followers = data.followers;
        this.following = data.followings;
        this.posts = data.posts;
      })
      .catch(error => console.error(error));
      
    fetch('http://localhost:5001/get_posts', {
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
  },
  methods: {
    deletePost(article) {
      const index = this.articles.indexOf(article);
      if (index !== -1) {
        this.articles.splice(index, 1);
        fetch(`http://localhost:5001/delete_post/${article.id}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(response.statusText);
            }
          })
          .catch(error => {
            console.error(error);
            this.articles.splice(index, 0, article);
          });
      }
    },
    editPost(article) {
      // Navigate to the edit post page with the article ID
      this.$router.push(`/editpost/${article.id}`);
    },
    exportData() {
  fetch('http://localhost:5001/export', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`
    }
  })
    .then(response => response.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'posts.csv');
      document.body.appendChild(link);
      link.click();
    })
    .catch(error => console.error(error));
},   
    }}

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