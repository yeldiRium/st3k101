<template>
    <div id="app">
        <router-view />
        <Dialog />
        <LoadingSpinnerModal
                :size="width"
        />
    </div>
</template>

<script>
    import {mapState} from "vuex";

    import Dialog from "./Partials/Modal/Dialog";

    export default {
        components: {
            Dialog
        },
        computed: {
            ...mapState("global", ["window"]),
            width() {
                if (this.window.width * .5 < 200) {
                    return "50%";
                }
                return "200px";
            }
        }
    };
</script>

<style lang="scss">
    @import "./scss/_variables";

    * {
        color: $verydark;
    }
</style>
