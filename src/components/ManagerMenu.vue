<template>
    <div class="container my-5">

        <div class="row mt-3">
            <div class="col-md-3" v-for="product in products" :key="product.id" :value="product.id">

                <div class="card">
                    <div class="card-body">
                        <img :src="'http://127.0.0.1:5000/download/' + product.upload_id" class="img-thumbnail rounded-4"
                            style="border: none; 
  background-color: transparent;" alt="">
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
    name: "ManagerMenu",
    data() {
        return {
            products: [],
            total_price: 0

        }
    },
    methods: {
        fetchItems() {

            axios.get("http://127.0.0.1:5000/getmanitems/" + this.$store.state.user_id, {
                headers: { Authorization: `Bearer ${this.$store.state.token}` }
            })
                .then(response => {
                    this.products = response.data.products;
                    this.total_price = response.data.total_price;

                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
        },
    },
    mounted() {
        this.fetchItems()
    },
    updated() {
        this.fetchItems()
    }
}
</script>
