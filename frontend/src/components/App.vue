<template>
    <div id="app">
        <router-view />
        <notifications
                position="top right"
        />
        <Dialog />
        <LoadingSpinnerModal
                :size="width"
        />
        <CreateQuestion/>
        <CreateDimension/>
        <CreateQuestionnaire/>
    </div>
</template>

<script>
    import {mapState} from "vuex";

    import Dialog from "./Partials/Modal/Dialog";
    import CreateQuestion from "./Partials/Modal/CreateQuestion";
    import CreateDimension from "./Partials/Modal/CreateDimension";
    import CreateQuestionnaire from "./Partials/Modal/CreateQuestionnaire";

    export default {
        components: {
            Dialog,
            CreateQuestion,
            CreateDimension,
            CreateQuestionnaire
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
