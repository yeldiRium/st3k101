<template>
    <div class="TestRange_container">
        <Toggle v-model="on1"
        >
            <template slot="off">
                Off
            </template>
            <template slot="on">
                On
            </template>
        </Toggle>
        <Toggle v-model="on2"
                :disabled="true"
        >
            <template slot="off">
                Off
            </template>
            <template slot="on">
                On
            </template>
        </Toggle>
        <Toggle v-model="on3"
                :disabled="true"
        >
            <template slot="off">
                Off
            </template>
            <template slot="on">
                On
            </template>
        </Toggle>
    </div>
</template>

<script>
    import Toggle from "../../Partials/Form/Toggle";

    export default {
        name: "TestToggle",
        components: {
            Toggle
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
    .TestRange_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .toggle {
        width: 400px;
        margin-bottom: 20px;
    }
</style>