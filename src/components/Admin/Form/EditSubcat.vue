<template >
    <div>
        <!-- Modal -->
        <div class="modal fade" id="editsubcat" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true"
            data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Add New Category</h5>
                    </div>
                    <div class="modal-body">
                        <div v-if="editsuccess" class="alert alert-success">
                            {{ editsuccess }}
                        </div>
                        <div v-else>
                            <div v-if="flashMessages" class="alert alert-danger">
                                {{ flashMessages }}
                            </div>
                            <form ref="editsubcatForm" class="needs-validation" novalidate>
                                <div class="mb-3">
                                    <label for="floatingSelect">Select Category</label>
                                    <select @click="fetchCat" class="form-select" id="floatingSelect" v-model="cat_id"
                                        aria-label="Floating label select example">
                                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                                            {{ cat.name }}
                                        </option>
                                    </select>

                                </div>
                                <div class="mb-3">
                                    <label for="floatingSelect">Select Subcategory</label>
                                    <select @click="fetchSubcat" class="form-select" id="floatingSelect" v-model="subcat_id"
                                        aria-label="Floating label select example">
                                        <option v-for="subcat in subcategories" :key="subcat.id" :value="subcat.id">
                                            {{ subcat.name }}
                                        </option>
                                    </select>

                                </div>
                                <div class="form-floating mb-3">
                                    <input v-model="name" type="text" class="form-control" id="subcatname"
                                        placeholder="Amul Milk" maxlength="50" required>
                                    <label for="subcatname">Subcategory Name</label>
                                </div>
                                <div class="mb-3">
                                    <label for="subcatfile" class="form-label">Upload Product Image</label>
                                    <input class="form-control" type="file" id="subcatfile" ref="fileInput"
                                        @change="handleFileChange">
                                </div>
                            </form>
                        </div>
                    </div>
                    <div v-if="!(editsuccess)">
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary" @click="editSubcat">
                                Edit </button>

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
    name: 'AddSubcat',
    data() {
        return {
            name: '',
            image_file: null,
            flashMessages: '',
            editsuccess: '',
            categories: [],
            subcategories: [],
            cat_id: '',
            subcat_id: '',
        };
    },

    methods: {
        auth() {
            this.editsuccess = ''
            this.image_file = '';
            this.name = '';
        },
        fetchCat() {
            axios.get("http://127.0.0.1:5000/categories")
                .then(response => {
                    this.categories = response.data.categories;
                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
        },
        fetchSubcat() {
            axios.get("http://127.0.0.1:5000/subcategories/" + this.cat_id)
                .then(response => {
                    this.subcategories = response.data.subcategories;
                })
                .catch(error => {
                    console.error("Error fetching subcategories:", error);
                });
        },
        handleFileChange(event) {
            // Update the selectedFile data property when the file input changes
            this.image_file = event.target.files[0];
        },
        editSubcat() {
            const form = this.$refs.editsubcatForm;

            if (form.checkValidity()) {
                const formData = new FormData();
                formData.append('name', this.name);
                formData.append('cat_id', this.cat_id);
                formData.append('image_file', this.image_file);


                // Make a POST request to your Flask backend
                axios.post("http://127.0.0.1:5000/subcatedit/admin/" + this.subcat_id, formData, {
                    headers: { Authorization: `Bearer ${this.$store.state.token}` }
                })
                    .then((response) => {
                        // Handle the response from the server
                        console.log(response.data);
                        const messages = response.data.flash
                        const editsuccess = response.data.success

                        // Update flashed messages
                        this.flashMessages = messages;
                        this.editsuccess = editsuccess
                        // If there are no error messages, clear the form

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