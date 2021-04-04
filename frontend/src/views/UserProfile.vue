<template>

  <div class="userprofile">
      <v-container>
        <v-row>

          <v-col>
            <h3>Name: {{ username }}</h3>
            <h3>Code: {{ code }}</h3>
          </v-col>

        </v-row>  
      </v-container>
  </div>

  
</template>

<script>
const axios = require('axios');
// import jwt_decode from "jwt-decode";

export default {
  name: 'UserProfile',
  data() {
    return {
      username: null,
      code: null
    }
  },
  created() {
      this.username = this.$store.state.userInfo.username;
      this.code = this.$store.state.userInfo.code;
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