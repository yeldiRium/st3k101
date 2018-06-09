<template>
    <div class="TestRange_container">
        <PrivateMenuBar />
    </div>
</template>

<script>
    import PrivateMenuBar from "../../Partials/Menu/PrivateMenuBar";

    export default {
        name: "TestRange",
        components: {
            PrivateMenuBar
        }
    }
</script>

<style lang="scss">
    .TestRange_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .privatemenubar {
        width: 90vw;
        height: 15vh;
    }
</style>