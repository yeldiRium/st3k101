<template>
    <div class="TestLoadingSpinner_container">
        <LoadingSpinner />
        <Button
                @click="buttonHandler"
        >
            Click to load for 5s.
        </Button>
        <LoadingSpinnerModal />
    </div>
</template>

<script>
    import LoadingSpinner from "../../Partials/LoadingSpinner";
    import LoadingSpinnerModal from "../../Partials/Modal/Loading";
    import Button from "../../Partials/Form/Button";

    export default {
        name: "TestLoadingSpinner",
        components: {
            LoadingSpinner,
            LoadingSpinnerModal,
            Button
        },
        methods: {
            buttonHandler() {
                this.$modal.show("loading");
                window.setTimeout(function() {
                    this.$modal.hide("loading");
                }.bind(this), 5000);
            }
        }
    }
</script>

<style lang="scss">
    .TestLoadingSpinner_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;

        > .loading-spinner {
            width: 300px;
        }
    }
</style>
