<template>
    <div id="app">
        <router-view />
        <Dialog />
    </div>
</template>

<script>
    import Dialog from "./Partials/Modal/Dialog";

    export default {
        components: {
            Dialog
        }
    };
</script>

<style lang="scss">
    @import "./scss/_variables";

    * {
        color: $verydark;
    }
</style>
