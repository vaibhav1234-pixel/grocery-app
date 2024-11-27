<template>
    <div class="container mt-5">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title">User Login</h4>
            </div>
            <div class="card-body">
                <div v-if="flashMessages" class="alert alert-danger">{{ flashMessages }}</div>
                <form ref="loginForm" class="needs-validation" novalidate>
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input v-model="username" type="text" class="form-control" id="username"
                            placeholder="Enter your username" required>
                        <div class="invalid-feedback">
                            Please enter a valid username.
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="userpassword" class="form-label">Password</label>
                        <input v-model="password" type="password" class="form-control" id="userpassword"
                            placeholder="Enter your password" minlength="6" required>
                        <div class="invalid-feedback">
                            Password must be longer than 6 characters.
                        </div>
                    </div>

                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary" @click="loginUser">Login</button>
                        <button type="button" class="btn btn-secondary" @click="$router.push({ name: 'signup' })">Sign
                            Up?</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from "axios";


export default {
    name: 'UserLogin',
    data() {
        return {
            username: '',
            password: '',
            flashMessages: '',
            token_vuex: ''

        };
    },

    methods: {
        loginUser() {
            const form = this.$refs.loginForm;

            if (form.checkValidity()) {
                const formData = new FormData();
                formData.append('username', this.username);
                formData.append('password', this.password);

                axios.post("http://127.0.0.1:5000/userlogin", formData)
                    .then((response) => {
                        const messages = response.data.error;


                        this.flashMessages = messages;


                        if (!this.flashMessages) {
                            const token = response.data.access_token;
                            const user_id = response.data.user_id;
                            const roles = response.data.roles;
                            this.$store.commit('setToken', token)
                            this.$store.commit('setUserId', user_id)
                            this.$store.commit('setRoles', roles)

                        }


                        if (!messages) {
                            this.username = '';
                            this.password = '';
                        }

                        if (this.$store.state.token) {
                            if (this.$store.state.roles.includes('user'))
                                // Redirect to the home component
                                this.$router.push({ name: 'home' });
                            if (this.$store.state.roles.includes('manager'))
                                // Redirect to the home component
                                this.$router.push({ name: 'manager_dashboard' });
                            if (this.$store.state.roles.includes('admin'))
                                // Redirect to the home component
                                this.$router.push({ name: 'admin_dashboard' });

                        }
                    })
                    .catch((error) => {

                        // Handle other errors
                        console.error("Error:", error);

                    });
            } else {
                form.classList.add('was-validated');
            }
        },
    },
};
</script>
  
<style lang="">
    <!-- Your styles go here -->
  </style>
  