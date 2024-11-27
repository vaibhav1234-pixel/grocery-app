<template>
    <div class="container my-5">
        <div class="d-flex justify-content-between pb-2 border-bottom border-dark">
            <div class="display-6 text-left fw-bolder">Requests</div>

            <div class="btn-group" role="group" aria-label="Basic mixed styles example">
                <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addrequest">
                    + Add Request
                </button>
                <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editrequest">
                    Edit
                </button>
                <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#removerequest">
                    Remove
                </button>

            </div>
        </div>
        <div class="row mt-5" style="max-height: 50vh; overflow-y: scroll;">
            <div class="col-md-3" v-for="cat in categories" :key="cat.id" :value="cat.id">
                <div class="card">
                    <div class="card-body">
                        <p class="card-text text-center" v-if="cat.approval == 'rejected'">Category {{ cat.name }} Request is
                            Rejected.
                        </p>
                        <p class="card-text text-center" v-if="cat.approval == 'approved'">Category {{ cat.name }} Request is
                            Approved.
                        </p>
                        <p class="card-text text-center" v-else>{{ cat.approval }} for category {{
                            cat.name }} is pending.
                        </p>

                        <!-- <h5 class="card-title text-center">Fruits</h5> -->


                    </div>
                </div>

            </div>
            <div class="col-md-3" v-for="subcat in subcategories" :key="subcat.id" :value="subcat.id">
                <div class="card">
                    <div class="card-body">
                        <p class="card-text text-center" v-if="subcat.approval == 'rejected'">
                            Subcategory {{ subcat.name }} Request is Rejected.
                        </p>
                        <p class="card-text text-center" v-if="subcat.approval == 'approved'">Subcategory {{ subcat.name }}
                            Request is Accepted.
                        </p>
                        <p class="card-text text-center" v-else>{{ subcat.approval }} for subcategory {{
                            subcat.name }} is pending.
                        </p>
                        <!-- <h5 class="card-title text-center">Fruits</h5> -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <RequestFunctions />
</template>
<script>
import axios from "axios";

import RequestFunctions from "@/components/Manager/Form/RequestFunctions.vue"

export default {
    name: "RequestMan",
    data() {
        return {
            categories: [],
            subcategories: [],
        }
    },
    components: {
        RequestFunctions
    },
    methods: {

        fetchCat() {
            axios.get("http://127.0.0.1:5000/req_categories/manager")
                .then(response => {
                    this.categories = response.data.categories;
                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
        },
        fetchSubcat() {
            axios.get("http://127.0.0.1:5000/req_subcategories/manager")
                .then(response => {
                    this.subcategories = response.data.subcategories;
                })
                .catch(error => {
                    console.error("Error fetching subcategories:", error);
                });
        },


    },
    created() {
        this.fetchCat();
        this.fetchSubcat();

    }
}
</script>
