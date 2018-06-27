<template>
    <modal name="loading"
           :clickToClose="false"
           :width="size"
           :height="size"
    >
        <LoadingSpinner :style="style"/>
    </modal>
</template>

<script>
    import LoadingSpinner from "./LoadingSpinner";

    export default {
        name: "LoadingSpinnerModal",
        components: {
            LoadingSpinner
        },
        props: {
            size: {
                default: "400px"
            }
        },
        computed: {
            style() {
                return {
                    width: this.size,
                    height: this.size
                };
            }
        }
    }
</script>

<style lang="scss">

</style>
