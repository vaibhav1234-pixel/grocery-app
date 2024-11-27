<template>
    <div class="container my-5 ">
        <div class="display-6 text-left fw-bolder">Requests</div>
        <div class="row mt-5">
            <div class="col-md-3" v-for="cat in categories" :key="cat.id" :value="cat.id">
                <div class="card">
                    <div class="card-body">
                        <p class="card-text text-center">
                            {{ cat.approval }}for category {{ cat.name }}
                        </p>
                        <!-- <h5 class="card-title text-center">Fruits</h5> -->
                        <form ref="requestForm">

                            <button class="btn btn-outline-success mb-2 w-100" for="success-outlined"
                                @click="approveCat('approved', cat.id)">Approve</button>


                            <button class="btn btn-outline-danger w-100" for="danger-outlined"
                                @click="approveCat('rejected', cat.id)">Reject</button>
                        </form>

                    </div>
                </div>

            </div>
            <div class="col-md-3" v-for="subcat in subcategories" :key="subcat.id" :value="subcat.id">
                <div class="card">
                    <div class="card-body">
                        <p class="card-text text-center">
                            {{ subcat.approval }} for subcategory {{
                                subcat.name }}
                        </p>
                        <!-- <h5 class="card-title text-center">Fruits</h5> -->
                        <form ref='requestSubcatForm'>

                            <button type="submit" class="btn btn-outline-success mb-2 w-100" for="success-outlined"
                                @click="approveSubcat('approved', subcat.id)">Approve</button>


                            <button type="submit" class="btn btn-outline-danger w-100" for="danger-outlined"
                                @click="approveSubcat('rejected', subcat.id)">Reject</button>
                        </form>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";

export default {
    name: "RequestAdmin",
    data() {
        return {
            name: '',
            image_file: null,
            flashMessages: '',
            editsuccess: '',
            categories: [],
            subcategories: [],

        };
    },
    methods: {

        fetchCat() {
            axios.get("http://127.0.0.1:5000/req_categories/admin")
                .then(response => {
                    this.categories = response.data.categories;
                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
        },
        fetchSubcat() {
            axios.get("http://127.0.0.1:5000/req_subcategories/admin")
                .then(response => {
                    this.subcategories = response.data.subcategories;
                })
                .catch(error => {
                    console.error("Error fetching subcategories:", error);
                });
        },

        approveCat(approval, cat_id) {



            const formData = new FormData();
            formData.append('approval', approval);



            // Make a POST request to your Flask backend
            axios.post("http://127.0.0.1:5000/catedit/approval/" + cat_id, formData)
                .then((response) => {
                    // Handle the response from the server
                    console.log(response.data);

                    const editsuccess = response.data.success


                    this.editsuccess = editsuccess
                    // If there are no error messages, clear the form

                })
                .catch((error) => {
                    // Handle errors
                    console.error("Error:", error);
                });

        },
        approveSubcat(approval, subcat_id) {



            const formData = new FormData();
            formData.append('approval', approval);



            // Make a POST request to your Flask backend
            axios.post("http://127.0.0.1:5000/subcatedit/approval/" + subcat_id, formData)
                .then((response) => {
                    // Handle the response from the server
                    console.log(response.data);

                    const editsuccess = response.data.success


                    this.editsuccess = editsuccess
                    // If there are no error messages, clear the form

                })
                .catch((error) => {
                    // Handle errors
                    console.error("Error:", error);
                });

        },



    },
    created() {
        this.fetchCat();
        this.fetchSubcat();

    }

}
</script>
