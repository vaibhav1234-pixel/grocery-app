<template >
    <div>
        <!-- Add -->
        <div class="modal fade" id="addrequest" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Request To Admin</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#addcatrequest" data-bs-dismiss="modal">
                                Category
                            </button>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#addsubcatrequest" data-bs-dismiss="modal">
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
        <div class="modal fade" id="editrequest" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Request To Admin</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#editcatrequest" data-bs-dismiss="modal">
                                Category
                            </button>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#editsubcatrequest" data-bs-dismiss="modal">
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
        <div class="modal fade" id="removerequest" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Request To Admin</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#removecatrequest" data-bs-dismiss="modal">
                                Category
                            </button>
                            <button type="button" class="btn btn-primary w-100 mb-3" data-bs-toggle="modal"
                                data-bs-target="#removesubcatrequest" data-bs-dismiss="modal">
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

    <AddCatRequest />
    <AddSubcatRequest />
    <EditCatRequest />
    <EditSubcatRequest />
    <RemoveCatRequest />
    <RemoveSubcatRequest />
</template>
<script>

import AddCatRequest from "@/components/Manager/Form/AddCatRequest.vue"
import AddSubcatRequest from "@/components/Manager/Form/AddSubcatRequest.vue"
import EditCatRequest from "@/components/Manager/Form/EditCatRequest.vue"
import EditSubcatRequest from "@/components/Manager/Form/EditSubcatRequest.vue"
import RemoveCatRequest from "@/components/Manager/Form/RemoveCatRequest.vue"
import RemoveSubcatRequest from "@/components/Manager/Form/RemoveSubcatRequest.vue"


export default {
    name: 'RequestFunctions',
    components: {
        AddCatRequest,
        AddSubcatRequest,
        EditCatRequest,
        EditSubcatRequest,
        RemoveCatRequest,
        RemoveSubcatRequest
    }
}
</script>
<style lang="">
    
</style>