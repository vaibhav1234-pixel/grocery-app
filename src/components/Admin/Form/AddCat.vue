<template >
    <div>
        <!-- Modal -->
        <div class="modal fade" id="addcat" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true"
            data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Add New Category</h5>
                    </div>
                    <div class="modal-body">
                        <div v-if="success" class="alert alert-success">
                            {{ success }}
                        </div>
                        <div v-else>
                            <div v-if="flashMessages" class="alert alert-danger">
                                {{ flashMessages }}
                            </div>
                            <form ref="catForm" class="needs-validation" novalidate>
                                <div class="form-floating mb-3">
                                    <input v-model="name" type="text" class="form-control" id="catname"
                                        placeholder="Amul Milk" maxlength="50" required>
                                    <label for="catname">Category Name</label>
                                </div>
                                <div class="mb-3">
                                    <label for="catfile" class="form-label">Upload Product Image</label>
                                    <input class="form-control" type="file" id="catfile" ref="fileInput"
                                        @change="handleFileChange" required>
                                </div>
                            </form>
                        </div>
                    </div>
                    <div v-if="!(success)">
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary" @click="addCat">
                                Add </button>

                        </div>
                    </div>
                    <div v-else>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" @click="auth">OK</button>
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
    name: 'AddCat',
    data() {
        return {
            name: '',
            image_file: null,
            flashMessages: '',
            success: ''
        };
    },

    methods: {
        auth() {
            this.success = ''
        },
        handleFileChange(event) {
            // Update the selectedFile data property when the file input changes
            this.image_file = event.target.files[0];
        },
        addCat() {


            const form = this.$refs.catForm;

            if (form.checkValidity()) {
                const formData = new FormData();
                formData.append('name', this.name);
                formData.append('image_file', this.image_file);



                // Make a POST request to your Flask backend
                axios.post("http://127.0.0.1:5000/catcreate/admin", formData, {
                    headers: { Authorization: `Bearer ${this.$store.state.token}` }
                })
                    .then((response) => {
                        // Handle the response from the server
                        console.log(response.data);
                        const messages = response.data.flash
                        const success = response.data.success

                        // Update flashed messages
                        this.flashMessages = messages;
                        this.success = success
                        // If there are no error messages, clear the form
                        if (!messages) {
                            this.image_file = '';
                            this.name = '';

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