<template>
    <div>
      <NavBar />
      <div class="container-fluid mt-5">
        <div class="row justify-content-center">
          <div class="col-sm-12 col-md-8 col-lg-6">
            <div class="card mx-auto">
              <div class="card-body">
                <h5 class="card-title">Edit Post</h5>
                <hr>
                <form>
                  <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" class="form-control" id="title" v-model="post.title">
                  </div>
                  <div class="form-group">
                    <label for="text">Text</label>
                    <textarea class="form-control" id="text" rows="5" v-model="post.text"></textarea>
                  </div>

                  <button type="button" class="btn btn-primary" @click="saveChanges">Save Changes</button>
                </form>
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
        post: {
          id: '',
          title: '',
          text: '',
          image_url: '',
          timestamp: ''
        }
      };
    },
    mounted() {
      // Fetch post data from server and populate post object
      const postId = this.$route.params.id;
      console.log(postId);
      fetch(`http://localhost:5001/pdit/${postId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log(data)
          this.post = {
            id: data.id,
            title: data.title,
            text: data.text,
            
          }
        })
        .catch(error => console.error(error));
    },
    methods: {
      saveChanges() {
        // Send updated post data to server and redirect to post details page
        fetch(`http://localhost:5001/edit/${this.post.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            title: this.post.title,
            text: this.post.text,
          })
        })
          .then(() => {
            this.$router.push(`/profile`);
          })
          .catch(error => console.error(error));
      }
    }
  }
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
  
  .form-group label {
    font-weight: bold;
  }
  
  .form-group input,
  .form-group textarea {
    margin-bottom: 1rem;
  }
  
  .btn-primary {
    margin-top: 1rem;
  }
  </style>
  