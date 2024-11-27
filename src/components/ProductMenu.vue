<template>
    <div class="container my-5">

        <div class="row mt-3">
            <div class="col-md-3" v-for="product in products" :key="product.id" :value="product.id">
                <div class="card" style=" cursor: pointer;" @click="navigateToProduct(product.id)">
                    <div class="card-body">
                        <img :src="'http://127.0.0.1:5000/download/' + product.upload_id" class="img-thumbnail rounded-4"
                            style="border: none; background-color: transparent;" alt="">
                        <div class="row mt-3 justify-content-between">
                            <div class="col-md-auto">
                                <h5 class="font-weight-bold">{{ product.name }}</h5>
                            </div>
                            <div class="col-md-auto">
                                <h5 class="font-weight-bold">Price: ₹{{ product.price }}</h5>
                            </div>
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
    name: "ProductMenu",
    data() {
        return {
            products: []
        }
    },
    methods: {
        fetchProduct() {
            if (this.$route.params.subcategoryId) {
                axios.get("http://127.0.0.1:5000/products/" + this.$route.params.subcategoryId)
                    .then(response => {
                        this.products = response.data.products;
                    })
                    .catch(error => {
                        console.error("Error fetching products:", error);
                    });
            } else {
                axios.get("http://127.0.0.1:5000/products/0")
                    .then(response => {
                        this.products = response.data.products;
                    })
                    .catch(error => {
                        console.error("Error fetching products:", error);
                    });
            }
        },

        navigateToProduct(productId) {
            this.$router.push({ path: `/product/${productId}` });
        },

    },
    mounted() {
        this.fetchProduct()
    }
}
</script>
