<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
    <v-container>
      <v-row>
        <div class="d-flex align-center" @click="$router.push({name: 'Home'})">
          <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
            transition="scale-transition"
            width="40"
          />

          <v-img
            alt="Vuetify Name"
            class="shrink mt-1 hidden-sm-and-down"
            contain
            min-width="100"
            src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
            width="100"
          />
        </div>
        
        <v-spacer></v-spacer>

        <div class="d-flex align-center">
          <v-btn v-if="$store.state.userInfo.userAccessToken != null" text @click="$router.push({name: 'UserProfile'})">
            <span class="mr-2">Profile</span>
          </v-btn>
          <v-btn v-if="$store.state.userInfo.userAccessToken != null" text @click="logout()">
            <span class="mr-2">Logout</span>
          </v-btn>
        </div>
      </v-row>
    </v-container>
    
    </v-app-bar>


    <div style="margin-top: 100px;">
      <v-container>
        <router-view/>
      </v-container>
    </div>

  </v-app>
</template>

<script>
export default {
  name: 'App',

  components: {
  },

  data: () => ({
  }),

  methods: {
    logout: function () {
      this.$store.commit('destroyToken');
      window.location.reload();
    }
  }
};
</script>
