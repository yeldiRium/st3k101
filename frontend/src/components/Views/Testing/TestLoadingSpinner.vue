<template>
    <div class="TestLoadingSpinner_container">
        <LoadingSpinner />
    </div>
</template>

<script>
    import LoadingSpinner from "../../Partials/LoadingSpinner";

    export default {
        name: "TestLoadingSpinner",
        components: {
            LoadingSpinner
        }
    }
</script>

<style lang="scss">
    .TestLoadingSpinner_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;

        .loading-spinner {
            width: 500px;
        }
    }
</style>
