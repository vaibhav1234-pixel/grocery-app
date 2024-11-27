<template >
    <div>
        <!-- Modal -->
        <div class="modal fade" id="addproduct" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true"
            data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Add New Producct</h5>
                    </div>
                    <div class="modal-body">
                        <div v-if="successProduct" class="alert alert-success">
                            {{ successProduct }}
                        </div>
                        <div v-else>
                            <div v-if="flashMessages" class="alert alert-danger">
                                {{ flashMessages }}
                            </div>
                            <form ref="productForm" class="needs-validation" novalidate>
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
                                    <input type="text" class="form-control" id="productname" placeholder="Amul Milk"
                                        required maxlength="20" minlength="2" v-model="name">
                                    <label for="productname">Product Name</label>
                                </div>


                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control" id="productprice" placeholder="Product Price"
                                        required v-model="price">
                                    <label for="productprice">Price</label>
                                </div>

                                <div class="form-floating mb-3">
                                    <textarea class="form-control" rows="4" placeholder="Amul Milk without cream 500ml"
                                        id="productdescription" maxlength="500" v-model="description"></textarea>
                                    <label for="productdescription">Description</label>
                                </div>

                                <div class="form-floating mb-3">
                                    <input type="date" class="form-control" id="productexpiry" placeholder="12-01-2023"
                                        required v-model="expiry">
                                    <label for="productexpiry">Product Expiry Date (in YYYY-MM-DD)</label>
                                </div>
                                <div class="mb-3">
                                    <label for="status">Status</label>
                                    <select @click="fetchSubcat" class="form-select" id="status" v-model="status"
                                        aria-label="Floating label select example">
                                        <option>In Stock</option>
                                        <option>Out of Stock</option>
                                    </select>

                                </div>
                                <div class="mb-3">
                                    <label for="subcatfile" class="form-label">Upload Product Image</label>
                                    <input class="form-control" type="file" id="subcatfile" ref="fileInput"
                                        @change="handleFileChange" required>
                                </div>
                            </form>
                        </div>
                    </div>
                    <div v-if="!(successProduct)">
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary" @click="addProduct">
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
    name: 'ManProdform',
    data() {
        return {
            name: '',
            expiry: '',
            description: '',
            price: '',
            image_file: null,
            flashMessages: '',
            successProduct: '',
            categories: [],
            subcategories: [],
            cat_id: '',
            subcat_id: '',
            status: ""
        };
    },

    methods: {
        auth() {
            this.successProduct = ''
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
        addProduct() {
            const form = this.$refs.productForm;

            if (form.checkValidity()) {
                const formData = new FormData();
                formData.append('name', this.name);
                formData.append('subcat_id', this.subcat_id);
                formData.append('image_file', this.image_file);
                formData.append('expiry', this.expiry);
                formData.append('description', this.description);
                formData.append('price', this.price);
                formData.append('status', this.status);
                formData.append('user_id', this.$store.state.user_id);




                // Make a POST request to your Flask backend
                axios.post("http://127.0.0.1:5000/product_create", formData, {
                    headers: { Authorization: `Bearer ${this.$store.state.token}` }
                })
                    .then((response) => {
                        // Handle the response from the server
                        console.log(response.data);
                        const messages = response.data.flash
                        const successProduct = response.data.success

                        // Update flashed messages
                        this.flashMessages = messages;
                        this.successProduct = successProduct
                        // If there are no error messages, clear the form
                        if (!messages) {
                            this.image_file = '';
                            this.name = '';
                            this.description = '',
                                this.expiry = '',
                                this.price = ''

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