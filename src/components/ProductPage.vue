<template>
    <div class="container my-5">
        <div class="row mt-3 border rounded-4 align-items-initial">
            <div class="col-md-6 border rounded-4" v-for="product in products" :key="product.id" :value="product.id">
                <div class="card" style="border: none;">
                    <div class="card-body">
                        <img :src="'http://127.0.0.1:5000/download/' + product.upload_id"
                            class="img-thumbnail rounded-4 mb-2" style="border: none; 
  background-color: transparent;" alt="">
                        <h5 class="card-title ms-2">{{ product.price }}</h5>
                        <h6 class="card-title ms-2">{{ product.status }}</h6>
                        <h6 class="card-title ms-2">{{ this.orders }}</h6>
                        <p class="card-text ms-2">{{ product.description }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mt-3" v-for="product in products" :key="product.id" :value="product.id">
                <div class="display-4">{{ product.name }}</div>
                <div class="lead">We are even faster than Flash!</div>
                <div v-if="added">
                    <button class="btn btn-warning my-2 w-100">Product Added</button>
                </div>
                <div v-else>
                    <div v-if="this.$store.state.token">
                        <button class="btn btn-warning my-2 w-100" @click="addToCart">ADD</button>
                    </div>
                    <div v-else>
                        <button class="btn btn-warning my-2 w-100" @click="$router.push({ name: 'login' })">Login</button>
                    </div>

                </div>


            </div>
        </div>
    </div>
</template>


<script>

import axios from "axios";

export default {
    name: "ProductPage",
    data() {
        return {
            products: [],
            added: '',
            orders: ''
        }
    },
    methods: {

        fetchProduct() {
            axios.get("http://127.0.0.1:5000/product/" + this.$route.params.productId)
                .then(response => {
                    this.products = response.data.products;
                })
                .catch(error => {
                    console.error("Error fetching products:", error);
                });
        },
        fetchProductCount() {
            axios.get("http://127.0.0.1:5000/totalitems/" + this.$route.params.productId, {
                headers: { Authorization: `Bearer ${this.$store.state.token}` }
            })
                .then(response => {
                    this.orders = response.data.total_orders;
                })
                .catch(error => {
                    console.error("Error fetching products:", error);
                });
        },
        addToCart() {
            axios.post("http://127.0.0.1:5000/addtocart/" + this.$route.params.productId + '/' + this.$store.state.user_id, null, {
                headers: { Authorization: `Bearer ${this.$store.state.token}` }
            })
                .then(response => {
                    const flash = response.data.message;
                    console.log(flash)
                    this.added = 'success'
                })
                .catch(error => {
                    console.error("Error fetching products:", error);
                });
        },

    },

    mounted() {
        this.fetchProduct()
        this.fetchProductCount()
    },
    updated() {
        this.fetchProductCount()
    }
}
</script>
