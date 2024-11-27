<template >
    <div>
        <!-- Modal -->
        <div class="modal fade" id="loginadmin" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">User Login</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div v-if="success" class="alert alert-success">
                            {{ success }}
                        </div>
                        <div v-else>
                            <div v-if="flashMessages" class="alert alert-danger">
                                {{ flashMessages }}
                            </div>

                            <form>
                                <div class="form-floating mb-3">
                                    <input v-model="email" type="email" class="form-control" id="adminloginemail"
                                        placeholder="Amul Milk" required>
                                    <label for="adminloginemail">Your Email</label>
                                </div>
                                <div class="form-floating mb-3">
                                    <input v-model="password" type="password" class="form-control" id="adminloginpassword"
                                        placeholder="Amul Milk" required>
                                    <label for="adminloginpassword">Password</label>
                                </div>


                            </form>

                        </div>

                    </div>
                    <div v-if="!(success)">
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary" @click="loginAdmin">Log
                                In</button>

                        </div>
                    </div>
                    <div v-else>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">OK</button>

                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>
<script>

import axios from "axios";


export default {
    name: 'LoginUser',
    data() {
        return {
            email: '',
            password: '',
            flashMessages: '',
            success: ''
        };
    },

    // props: {
    //     getAuth: Function,

    // },

    methods: {
        managerUser() {
            const form = this.$refs.signupForm;

            if (form.checkValidity()) {
                // Get the values from the data properties
                const email = this.email;
                const password = this.password;


                // Make a POST request to your Flask backend
                axios.post("http://127.0.0.1:5000/login", {
                    email: email,
                    password: password,

                })
                    .then((response) => {
                        // Handle the response from the server
                        console.log(response.data);
                        const messages = response.data.flash;
                        const success = response.data.success

                        // Update flashed messages
                        this.flashMessages = messages;
                        this.success = success
                        // If there are no error messages, clear the form
                        if (!messages) {
                            this.email = '';
                            this.password = '';

                            // this.$router.push({ name: 'home' });



                        }
                    })
                    .catch((error) => {
                        // Handle errors
                        console.error("Error:", error);
                    });
            } else {
                // If the form is not valid, show the validation messages
                form.classList.add('was-validated');
            }
        },
    },

}
</script>
<style lang="">
    
</style>