import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import UserProfile from '../views/UserProfile.vue'
import store from '../store/index'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: (to, from , next) => {
      if (store.state.userInfo.userAccessToken == null)next({name: 'Login'})
      else next()
    }
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile,
    beforeEnter: (to, from , next) => {
      if (store.state.userInfo.userAccessToken == null)next({name: 'Login'})
      else next()
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    beforeEnter: (to, from , next) => {
      if (store.state.userInfo.userAccessToken != null) next({name: 'Home'})
      else next()
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    beforeEnter: (to, from , next) => {
      if (store.state.userInfo.userAccessToken != null) next({name: 'Home'})
      else next()
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
