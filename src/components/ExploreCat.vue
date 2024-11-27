<template>
    <div class="container my-5">

        <div class="row mt-3">
            <div class="col-md-3" v-for="cat in categories" :key="cat.id" :value="cat.id">
                <div class="card" style="border: none; cursor: pointer;" @click="navigateToSubcategories(cat.id)">
                    <div class="card-body">
                        <img :src="'http://127.0.0.1:5000/download/' + cat.upload_id" class="img-thumbnail rounded-4"
                            style="border: none; background-color: transparent;" alt="">

                        <!-- <img :src="getCategoryImageUrl(category.img)" :alt="category.name"> -->
                        <h5 class="card-title text-center">{{ cat.name }}</h5>
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

    name: "ExploreCat",
    data() {
        return {
            categories: []
        }
    },
    methods: {

        fetchCat() {

            axios.get("http://127.0.0.1:5000/categories")
                .then(response => {
                    this.categories = response.data.categories;
                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
        },
        navigateToSubcategories(categoryId) {
            this.$router.push({ path: `/subcategories/${categoryId}` });
        },


    },
    mounted() {
        this.fetchCat()
    },
    updated() {
        this.fetchCat()
    },


}

</script>
