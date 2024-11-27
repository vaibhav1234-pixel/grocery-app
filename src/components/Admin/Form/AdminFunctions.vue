<template >
    <div>
        <!-- Add -->
        <div class="modal fade" id="add" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel"> To Admin</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#addcat" data-bs-dismiss="modal">
                                Category
                            </button>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#addsubcat" data-bs-dismiss="modal">
                                Sub-Category
                            </button>
                        </form>
                    </div>
                    <!-- <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Submit</button>
                    </div> -->
                </div>
            </div>
        </div>

    </div>
    <div>
        <!-- Edit -->
        <div class="modal fade" id="edit" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel"> To Admin</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#editcat" data-bs-dismiss="modal">
                                Category
                            </button>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#editsubcat" data-bs-dismiss="modal">
                                Sub-Category
                            </button>
                        </form>
                    </div>
                    <!-- <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Submit</button>
                    </div> -->
                </div>
            </div>
        </div>

    </div>
    <div>
        <!-- Remove -->
        <div class="modal fade" id="remove" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel"> To Admin</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#removecat" data-bs-dismiss="modal">
                                Category
                            </button>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#removesubcat" data-bs-dismiss="modal">
                                Sub-Category
                            </button>
                        </form>
                    </div>
                    <!-- <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Submit</button>
                    </div> -->
                </div>
            </div>
        </div>

    </div>

    <AddCat />
    <AddSubcat />
    <EditCat />
    <EditSubcat />
    <RemoveCat />
    <RemoveSubcat />
</template>
<script>

import AddCat from "@/components/Admin/Form/AddCat.vue"
import AddSubcat from "@/components/Admin/Form/AddSubcat.vue"
import EditCat from "@/components/Admin/Form/EditCat.vue"
import EditSubcat from "@/components/Admin/Form/EditSubcat.vue"
import RemoveCat from "@/components/Admin/Form/RemoveCat.vue"
import RemoveSubcat from "@/components/Admin/Form/RemoveSubcat.vue"


export default {
    name: 'AdminFunctions',
    components: {
        AddCat,
        AddSubcat,
        EditCat,
        EditSubcat,
        RemoveCat,
        RemoveSubcat
    }
}
</script>
<style lang="">
    
</style>