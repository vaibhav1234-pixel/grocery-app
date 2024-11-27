<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Grocery App</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">

                <ul class="navbar-nav ms-auto me-0">
                    <li class="nav-item">
                        <button type="button" class="btn btn-outline-warning me-3" @click="toCart">
                            Cart
                        </button>
                    </li>
                    <li class="nav-item">
                        <div v-if="this.$store.state.token">
                            <button type="button" class="btn btn-outline-dark" @click="logoutUser">
                                Logout
                            </button>

                        </div>
                        <div v-else>
                            <button type="button" class="btn btn-outline-dark" @click="$router.push({ name: 'signup' })">
                                Sign Up
                            </button>
                        </div>

                    </li>
                </ul>


            </div>
        </div>
    </nav>
</template>
<script>

import axios from "axios";

export default {
    name: 'NavBar',
    methods: {
        logoutUser() {
            axios.post("http://127.0.0.1:5000/userlogout", null, {
                headers: { Authorization: `Bearer ${this.$store.state.token}` }
            })
                .then((response) => {
                    const messages = response.data.message;

                    this.$store.commit('setToken', '')
                    this.$store.commit('setUserId', '')

                    this.$router.push({ name: 'home' });

                    console.log(messages);
                })
                .catch((error) => {
                    if (error.response && error.response.status === 401) {
                        // Handle authentication failure (e.g., show an error message to the user)
                        console.error("Authentication failed:", error.response.data.error);
                    } else {
                        // Handle other errors
                        console.error("Error:", error);
                    }
                });
        },
        toCart() {
            this.$router.push({ name: 'cartview', params: { 'userId': this.$store.state.user_id } });
        }


    },
}

</script>
<style></style>