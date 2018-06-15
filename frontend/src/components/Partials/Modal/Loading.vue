<template>
    <modal name="loading"
           :width="width"
           :height="width"
           :clickToClose="false"
    >
        <LoadingSpinner
                :style="style"
        />
    </modal>
</template>

<script>
    import {mapState} from "vuex";

    import LoadingSpinner from "../LoadingSpinner";

    export default {
        name: "Loading",
        components: {
            LoadingSpinner
        },
        computed: {
            ...mapState("global", ["window"]),
            width() {
                if (this.window.width * .5 < 200) {
                    return "50%";
                }
                return "200px";
            },
            style() {
                return {
                    width: this.width
                };
            }
        }
    }
</script>

<style lang="scss">

</style>
