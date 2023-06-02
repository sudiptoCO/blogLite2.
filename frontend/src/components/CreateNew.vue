<template>
  <div>
    <NavBar/>
    <div class="container">
      <h1 class="mb-4">Create Post Here</h1>
      <form>
        <div class="form-group">
          <label for="title" class="form-label">Title</label>
          <input type="text" class="form-control" id="title" v-model="title">
        </div>
        <div class="form-group">
          <label for="content" class="form-label">Content</label>
          <textarea class="form-control" id="content" rows="5" v-model="text"></textarea>
        </div>
        <div class="form-group">
          <label for="image" class="form-label">Image</label>
          <input type="file" class="form-control-file" id="image" ref="fileInput" @change="onFileChange">
        </div>
        <button type="submit" class="btn btn-primary mt-3" @click.prevent="createPost">Submit</button>
      </form>
      <div v-if="showSuccessMessage" class="alert alert-success mt-3" role="alert">
        Post added successfully!
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from './NavBar.vue';
export default {
  components: { NavBar },
  data() {
    return {
      title: '',
      text: '',
      image: null,
      showSuccessMessage: false
    }
  },
  methods: {
    onFileChange(event) {
      this.image = event.target.files[0];
    },
    createPost() {
      let formData = new FormData();
      formData.append('title', this.title);
      formData.append('text', this.text);
      formData.append('image', this.image);

      axios.post('http://localhost:5001/add_post', formData)
        .then(response => {
          console.log(response.data);
          this.showSuccessMessage = true;
          this.title = '';
          this.text = '';
          this.image = null;
        })
        .catch(error => {
          console.log(error.response.data);
        });
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  font-weight: bold;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0069d9;
  border-color: #0062cc;
}
</style>
