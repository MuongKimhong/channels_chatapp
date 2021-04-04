import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersist from 'vuex-persist'

const vuexPersist = new VuexPersist({
  key: 'myapp',
  storage: window.localStorage
})

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [vuexPersist.plugin],
  state: {
    userInfo: {
      userAccessToken: null,
      id: null,
      username: null,
      code: null
    },
    firstChatroomId: null,
    firstChatroomUser2Id: null,
    firstMessageId: null
  },
  mutations: {
    storeUserInfo: function(state, userInfo) {
      state.userInfo.userAccessToken = userInfo.access;
      state.userInfo.username = userInfo.username;
      state.userInfo.id = userInfo.id;
      state.userInfo.code = userInfo.code;
    },
    destroyToken: function(state) {
      for (var key in state.userInfo) {
        state.userInfo[key] = null;
      } 
    },
    getFirstChatroomId: function(state, id) {
      state.firstChatroomId = id;
    },
    getFirstChatroomUser2Id: function(state, id) {
      state.firstChatroomUser2Id = id;
    },
    getFirstMessageId: function(state, id) {
      state.firstMessageId = id;
    }
  },
  actions: {
  },
  modules: {
  }
})
