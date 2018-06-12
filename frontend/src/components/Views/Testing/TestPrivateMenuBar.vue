<template>
    <div class="TestMenuBarPrivate_container">
        <MenuBarPrivate />
    </div>
</template>

<script>
    import MenuBarPrivate from "../../Partials/Menu/MenuBarPrivate";

    export default {
        name: "TestRange",
        components: {
            MenuBarPrivate
        }
    }
</script>

<style lang="scss">
    .TestMenuBarPrivate_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .menu-bar-private {
        width: 90vw;
        height: 15vh;
    }
</style>