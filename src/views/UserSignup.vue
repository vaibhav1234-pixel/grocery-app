<template>
    <div class="container mt-5">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title">User Signup</h4>
            </div>
            <div class="card-body">
                <div v-if="flashMessages" class="alert alert-danger">{{ flashMessages }}</div>
                <form ref="signupForm" class="needs-validation" novalidate>
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input v-model="username" type="text" class="form-control" minlength="4" maxlength="20"
                            id="username" placeholder="Enter your username" required>
                        <div class="invalid-feedback">
                            Please enter a valid username.
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="useremail" class="form-label">Email</label>
                        <input v-model="email" type="email" class="form-control" id="useremail"
                            placeholder="Enter your email" required>
                        <div class="invalid-feedback">
                            Please enter a valid email.
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="userpassword" class="form-label">Password</label>
                        <input v-model="password" type="password" class="form-control" minlength="6" id="userpassword"
                            placeholder="Enter your password" required>
                        <div class="invalid-feedback">
                            Password must be longer than 6 characters.
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="userType" class="form-label">Select User Type</label>
                        <select v-model="userType" class="form-select" id="userType" required>
                            <option value="user">User</option>
                            <option value="manager">Manager</option>
                        </select>
                    </div>

                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary" @click="signUpUser">Sign Up</button>
                        <button type="button" class="btn btn-secondary" @click="$router.push({ name: 'login' })">Log
                            In?</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from "axios";

export default {
    name: 'UserSignup',
    data() {
        return {
            username: '',
            email: '',
            password: '',
            flashMessages: '',
            success: '',
            userType: '',
        };
    },

    methods: {
        signUpUser() {
            const form = this.$refs.signupForm;

            if (form.checkValidity()) {
                const formData = new FormData();
                formData.append('email', this.email);
                formData.append('username', this.username);
                formData.append('userType', this.userType);
                formData.append('password', this.password);

                axios.post("http://127.0.0.1:5000/usersignup", formData)
                    .then((response) => {
                        const messages = response.data.flash;
                        const success = response.data.success

                        this.flashMessages = messages;
                        this.success = success

                        if (this.success) {
                            // Redirect to the home component
                            this.$router.push({ name: 'login' });
                        }
                    })
                    .catch((error) => {
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
  