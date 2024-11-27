<template>
    <div class="container my-5">
        <div class="d-flex justify-content-between my-5 pb-2 border-bottom border-dark">
            <div class="display-6 text-left fw-bold">Products</div>

            <div class="btn-group" role="group" aria-label="Basic mixed styles example">
                <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addproduct">
                    + New Product
                </button>
                <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editproduct">
                    Edit
                </button>
                <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#removeproduct">
                    Remove
                </button>

            </div>

        </div>
        <ManagerMenu />

    </div>
    <ManProdform />
    <EditProduct />
    <RemoveProduct />
</template>
<script>

import ManProdform from "@/components/Manager/Form/ManProdform.vue"
import EditProduct from "@/components/Manager/Form/EditProduct.vue"
import RemoveProduct from "@/components/Manager/Form/RemoveProduct.vue"
import ManagerMenu from "@/components/ManagerMenu.vue"
export default {
    name: "ProductMan",
    components: {
        ManProdform,
        EditProduct,
        RemoveProduct,
        ManagerMenu
    }
}
</script>
