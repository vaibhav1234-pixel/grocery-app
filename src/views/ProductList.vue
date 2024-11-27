<template>
    <NavBar />
    <div class="display-1 text-center fw-bolder my-3">Explore Products</div>
    <ProductMenu />
</template>
<script>

import NavBar from "@/components/NavBar.vue"
import ProductMenu from "@/components/ProductMenu.vue"

export default {
    name: 'ProductList',
    components: {
        NavBar,
        ProductMenu

    }
}
</script>
<style lang="">
    
</style>