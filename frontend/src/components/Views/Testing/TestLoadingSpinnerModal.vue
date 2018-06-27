<template>
    <div class="TestLoadingSpinnerModal_container">
        <Button @click="handleClick">
            click me
        </Button>
    </div>
</template>

<script>
    import Future from "fluture";

    import Button from "../../Partials/Form/Button";

    export default {
        name: "TestToggle",
        components: {
            Button
        },
        methods: {
            handleClick(event) {
                this.$load(Future((reject, resolve) => {
                    window.setTimeout(resolve, 3000);
                })).fork(console.error, console.log);
            }
        }
    }
</script>

<style lang="scss">
    .TestLoadingSpinnerModal_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }
</style>