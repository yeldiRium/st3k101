<template>
    <div class="TestButton_container">
        <Button text="Dies ist ButtonText"
                @click="handler1"
        />
        <Button text="Noch mehr Buttontext"
                @click="handler2"
                :elevation="6"
        />
        <Button text="Ein abgehobener Button mit viel content."
                @click="handler2"
                :elevation="12"
        />
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