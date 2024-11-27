<template>
    <NavBar />
    <CartMenu />
</template>
<script>

import CartMenu from "@/components/CartMenu.vue"
import NavBar from "@/components/NavBar.vue"

export default {
    name: "CartView",
    components: {
        NavBar,
        CartMenu
    }
}
</script>
