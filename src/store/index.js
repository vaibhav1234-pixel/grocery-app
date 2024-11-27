import { createStore } from 'vuex'

export default createStore({
  state: {
    token: localStorage.getItem('token'),
    user_id: localStorage.getItem('user_id'),
    roles: [localStorage.getItem('roles')]
  },
  getters: {
  },
  mutations: {
    setToken(state, newToken) {
      state.token = newToken;
      localStorage.setItem('token', newToken);
    },
    setUserId(state, newUserId) {
      state.user_id = newUserId;
      localStorage.setItem('user_id', newUserId);
    },
    setRoles(state, newroles) {
      state.roles = newroles;
      localStorage.setItem('roles', newroles)
    },
  },
  actions: {
  },
  modules: {
  }
})
