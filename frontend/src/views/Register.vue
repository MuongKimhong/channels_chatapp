<template>

  <div class="register">
      <v-container>
        <v-row class="justify-center">

          <v-col class="col-lg-6 col-md-6 col-sm-8">
            <v-card class="py-5 px-5" elevation=5>
              <h2 class="text-center">Register</h2>

              <v-card v-if="error" color="red darken-2" class="py-5 px-5 col-12 my-5">
                <h4 class="white--text text-center">{{ errorText }}</h4>
              </v-card>

              <form @submit.prevent="register()">
                <v-text-field v-model="username" type="text" label="Username"></v-text-field>
                <v-text-field v-model="password" type="password" label="Password"></v-text-field>
                <v-text-field v-model="confirmPassword" type="password" label="Confirm Password"></v-text-field>

                <small class="ml-auto" style="cursor: pointer">show password</small>

                <div class="mt-4">
                  <v-btn type="submit" class="col-12" color="primary" elevation=5>Register</v-btn>
                  <router-link to="/login">
                    <h5 class="mt-3 text-center">login</h5>
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
export default {
  name: 'Register',
  data() {
    return {
      username: null,
      password: null,
      confirmPassword: null,

      error: false,
      errorText: null
    }
  },
  methods: {
    register: function () {
      if (this.password != this.confirmPassword) {
        this.error = true;
        this.errorText = "Two password didn't match";
        return;
      }

      axios.post('http://localhost:8000/api/register/', {
        username: this.username,
        password: this.password
      })
      .then((response) => {
        if (response.data.success) this.$router.push({name: 'Login'})
      })
      .catch((error) => {
        this.error = true;
        this.errorText = error.response.data.error;
      })
    }
  }
}
</script>
