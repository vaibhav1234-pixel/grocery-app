<template>
    <NavBar />
    <div class="display-1 text-center fw-bolder my-3">Explore Sub-Categories</div>
    <SubCat />
</template>
<script>

import NavBar from "@/components/NavBar.vue"
import SubCat from "@/components/SubCat.vue"

export default {
    name: 'SubcatView',
    components: {
        NavBar,
        SubCat

    }
}
</script>
<style lang="">
    
</style>