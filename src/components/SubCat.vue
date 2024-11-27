<template>
    <div class="container my-5">

        <div class="row mt-3">
            <div class="col-md-3" v-for="subcat in subcategories" :key="subcat.id" :value="subcat.id">
                <div class="card" style="border: none;cursor: pointer;" @click="navigateToProducts(subcat.id)">
                    <div class="card-body">
                        <img :src="'http://127.0.0.1:5000/download/' + subcat.upload_id" class="img-thumbnail rounded-4"
                            style="border: none; 
  background-color: transparent;" alt="">
                        <h5 class="card-title text-center">{{ subcat.name }}</h5>
                        <!-- <p class="card-text text-center">Mishra</p> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>

import axios from "axios";

export default {
    name: "SubCat",
    data() {
        return {
            subcategories: []
        }
    },
    methods: {
        fetchSubcat() {
            axios.get("http://127.0.0.1:5000/subcategories/" + this.$route.params.categoryId)
                .then(response => {
                    this.subcategories = response.data.subcategories;
                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
        },
        navigateToProducts(subcategoryId) {
            this.$router.push({ path: `/products/${subcategoryId}` });
        },

    },
    mounted() {
        this.fetchSubcat()
    }
}
</script>
