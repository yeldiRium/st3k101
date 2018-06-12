<template>
    <div class="TestToggleButton_container">
        <ToggleButton v-model="on1"
        >
            <template slot="off">
                Off
            </template>
            <template slot="on">
                On
            </template>
        </ToggleButton>
        <ToggleButton v-model="on2"
                :disabled="true"
        >
            <template slot="off">
                Off
            </template>
            <template slot="on">
                On
            </template>
        </ToggleButton>
        <ToggleButton v-model="on3"
                :disabled="true"
        >
            <template slot="off">
                Off
            </template>
            <template slot="on">
                On
            </template>
        </ToggleButton>
    </div>
</template>

<script>
    import ToggleButton from "../../Partials/Form/ToggleButton";

    export default {
        name: "TestToggle",
        components: {
            ToggleButton
        },
        data() {
            return {
                on1: true,
                on2: false,
                on3: true
            };
        }
    }
</script>

<style lang="scss">
    .TestToggleButton_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .toggle-button {
        width: 400px;
        margin-bottom: 20px;
    }
</style>