<template>
    <NavBar />
    <div class="display-1 text-center fw-bolder mt-5">E x p l o r e</div>
    <ExploreCat />
</template>


<script>

import NavBar from "@/components/NavBar.vue"

import ExploreCat from "@/components/ExploreCat.vue"

export default {
    name: 'HomeView',
    components: {
        NavBar,

        ExploreCat
    }
}
</script>
