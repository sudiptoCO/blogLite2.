<template>
  <div class="container mt-6">
    <h3 class="text-center mb-3 text-style">BlogLite</h3> 
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-md-6">
        <h3 class="mb-3">Sign up</h3>
        <form @submit.prevent="signup" class="card p-3">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" id="username" class="form-control" v-model="username" required>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" class="form-control" v-model="password" required>
          </div>
          <button type="submit" class="btn btn-primary">Sign up</button>
        </form>
        <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      error: null
    };
  },
  methods: {
    signup() {
      fetch("http://127.0.0.1:5001/add_user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: this.username,
          password: this.password
        })
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Sign up failed");
          }
        })
        .then(data => {
          console.log(data);
          alert("User added successfully!");
          this.$router.push("/login"); // Redirect to login page
        })
        .catch(error => {
          this.error = error.message;
        });
    }
  }
};
</script>

<style>
  .form-group {
    margin-bottom: 1rem;
  }

  .text-style {
    font-size: 30px !important;
    font-family: fantasy !important;
    color: mediumblue !important;
  }
</style>
