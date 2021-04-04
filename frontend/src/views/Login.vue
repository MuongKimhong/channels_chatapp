<template>

  <div class="login">
      <v-container>
        <v-row class="justify-center">

          <v-col class="col-lg-6 col-md-6 col-sm-8">
            <v-card class="py-5 px-5" elevation=5>
              <h2 class="text-center">Login</h2>

              <v-card v-if="error" color="red darken-2" class="py-5 px-5 col-12 my-5">
                <h4 class="white--text text-center">Username or password is incorrect</h4>
              </v-card>

              <form @submit.prevent="login()">
                <v-text-field v-model="username" required type="text" label="Username"></v-text-field>
                <v-text-field v-model="password" required type="password" label="Password"></v-text-field>
                <small class="ml-auto" style="cursor: pointer">show password</small>
                <div class="mt-4">
                  <v-btn type="submit" class="col-12" color="primary" elevation=5>Login</v-btn>
                  <router-link to="/register">
                    <h5 class="mt-3 text-center">Create an account</h5>
                  </router-link>
                </div>
              </form>
            </v-card>
          </v-col>

        </v-row>  
      </v-container>
  </div>

  
</template>

<script>
const axios = require('axios');
// import jwt_decode from "jwt-decode";

export default {
  name: 'Login',
  data() {
    return {
      username: null,
      password: null,
      error: false
    }
  },
  methods: {
    login() {
      axios.post('http://localhost:8000/api/token/', {
        username: this.username,
        password: this.password
      })
      .then((response) => {
        this.$store.commit('storeUserInfo', response.data);
        this.$router.push({name: 'Home'})
      })
      .catch((error) => {
        if (error) this.error = true;
      })
    }
  }
}
</script>
