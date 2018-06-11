<template>
    <div id="app">
        <router-view />
        <v-dialog />
    </div>
</template>

<script>
    export default {};
</script>

<style lang="scss">
    @import "./scss/_variables";

    * {
        color: $verydark;
    }
</style>
