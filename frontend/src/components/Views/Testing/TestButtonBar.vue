<template>
    <div class="TestButtonBar_container">
        <ButtonBar
        />
    </div>
</template>

<script>
    import ButtonBar from "../../Partials/Bars/ButtonBar";

    export default {
        name: "TestButtonBar",
        components: {ButtonBar}
    }
</script>

<style lang="scss">
    .TestButtonBar_container {
        margin-top: 100px;
        width: 400px;
        height: 400px;

        padding: 0;
    }
</style>