<template>
    <div class="authentication"
         :style="style"
    >
        blub
    </div>
</template>

<script>
    import {mapState} from "vuex";

    export default {
        name: "Authentication",
        created() {

        },
        computed: {
            ...mapState("global", ["window"])
        }
    }
</script>

<style lang="scss">

</style>
