<template>
    <div v-if="hasUserRole('admin')">
        <div>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="container-fluid">
                    <a class="navbar-brand" href="#">Admin Dashboard</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav ms-auto me-0">
                            <li class="nav-item">
                                <a class="nav-link" href="#">Features</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="#">Pricing</a>
                            </li>
                            <li class="nav-item">
                                <button class="btn btn-dark" @click="logoutUser">Logout</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
        <RequestAdmin />
        <CatAdmin />
        <SubCatAdmin />
    </div>
    <div v-else class="container d-flex align-items-center justify-content-center vh-100">
        <button class="btn btn-danger lg" @click="this.$router.push({ name: 'login' });">Login As Admin</button>
    </div>
</template>


<script>
import axios from 'axios'
import RequestAdmin from "@/components/Admin/RequestAdmin.vue"
import CatAdmin from "@/components/Admin/CatAdmin.vue"
import SubCatAdmin from "@/components/Admin/SubCatAdmin.vue"

export default {
    name: 'AdminExp',
    components: {
        RequestAdmin,
        CatAdmin,
        SubCatAdmin
    },
    methods: {
        hasUserRole(role) {
            return this.$store.state.roles.includes(role)
        },
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
    }
}
</script>