<template>
    <div class="TestButton_container">
        <Button @click="handler1">
            Dies ist ButtonText
        </Button>
        <Button @click="handler2"
                :elevation="6"
        >
            Noch mehr Buttontext
        </Button>
        <Button @click="handler2"
                :elevation="12"
        >
            Ein abgehobener Button mit viel content.
        </Button>
    </div>
</template>

<script>
    import Button from "../../Partials/Form/Button";

    export default {
        name: "TestButton",
        components: {
            Button
        },
        methods: {
            handler1() {
                alert("Button 1 clicked!");
            },
            handler2() {
                alert("Button 2 clicked!");
            },
            handler3() {
                alert("Button 3 clicked!");
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_elevation";

    .TestButton_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .button {
        margin-bottom: 20px;
    }
</style>