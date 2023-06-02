<template>
  <div class="container mt-6">
    <h3 class="text-center mb-3 text-style">BlogLite</h3> 
    <div class="row justify-content-center  align-items-center min-vh-100">
      <div class="col-md-6">
        
        <form @submit.prevent="login" class="card p-3">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" id="username" class="form-control" v-model="username" required>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" class="form-control" v-model="password" required>
          </div>
          <button type="submit" class="btn btn-primary">Log in</button>
        </form>
        <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
        <div class="text-center mt-3"> <!-- Centered text -->
          Don't have an account? 
          <router-link to="/signup" class="btn btn-link">Sign up here</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      error: null
    };
  },
  methods: {
    login() {
      fetch("http://localhost:5001/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Login failed");
          }
        })
        .then(data => {
          if (data.success) {
            // save the token in local storage
            localStorage.setItem('token', data.token);
            // handle successful login
            this.$router.push("/");
          } else {
            this.error = "Invalid username or password";
          }
        })
        .catch(error => {
          this.error = error.message;
        });
    }
  }
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
.text-center {
  text-align: center;
}
.text-style {
  font-size: 30px !important;
  font-family: fantasy !important;
  color: mediumblue !important;
}
</style>
