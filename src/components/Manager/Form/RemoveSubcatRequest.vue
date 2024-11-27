<template >
    <div>
        <!-- Modal -->
        <div class="modal fade" id="removesubcatrequest" tabindex="-1" aria-labelledby="exampleModalLabel"
            aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Remove Sub Category</h5>
                    </div>
                    <div class="modal-body">
                        <div v-if="removeSubcatSuccess" class="alert alert-success">
                            {{ removeSubcatSuccess }}
                        </div>
                        <div v-else>
                            <div v-if="flashMessages" class="alert alert-danger">
                                {{ flashMessages }}
                            </div>
                            <form ref="subcatRemoveRequestForm" class="needs-validation" novalidate>
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

                            </form>
                        </div>
                    </div>
                    <div v-if="!(removeSubcatSuccess)">
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary" @click.prevent="removeSubcat">
                                Remove </button>

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
            flashMessages: '',
            removeSubcatSuccess: '',
            categories: [],
            subcategories: [],
            cat_id: '',
            subcat_id: '',
        };
    },

    methods: {
        auth() {
            this.removeSubcatSuccess = ''
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
        removeSubcat() {
            const form = this.$refs.subcatRemoveRequestForm;

            if (form.checkValidity()) {


                // Make a POST request to your Flask backend
                axios.delete("http://127.0.0.1:5000/subcatremove/manager/" + this.subcat_id, {
                    headers: { Authorization: `Bearer ${this.$store.state.token}` }
                })
                    .then((response) => {
                        // Handle the response from the server
                        console.log(response.data);
                        const messages = response.data.flash
                        const removeSubcatSuccess = response.data.success

                        // Update flashed messages
                        this.flashMessages = messages;
                        this.removeSubcatSuccess = removeSubcatSuccess
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