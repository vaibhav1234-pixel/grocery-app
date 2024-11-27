<template>
    <div class="container my-5 pb-2 border-bottom border-dark">
        <div class="d-flex justify-content-between">
            <div class="display-6 text-left fw-bolder ">Categories</div>

            <div class="btn-group" role="group" aria-label="Basic mixed styles example">
                <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#add">
                    + Add
                </button>
                <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#edit">
                    Edit
                </button>
                <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#remove">
                    Remove
                </button>

            </div>
        </div>

    </div>

    <AdminFunctions />
</template>
<script>

import AdminFunctions from "@/components/Admin/Form/AdminFunctions.vue"

export default {
    name: "CatAdmin",
    components: {
        AdminFunctions
    }
}
</script>
