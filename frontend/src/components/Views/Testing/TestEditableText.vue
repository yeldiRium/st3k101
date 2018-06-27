<template>
    <div class="TestEditableText_container">
        <EditableText v-model="text1" :key="text1" /><br/><br/>
        <EditableText v-model="text2" :key="text2" /><br/><br/>
        <EditableText v-model="text3" :key="text3" /><br/><br/>
    </div>
</template>

<script>
    import EditableText from "../../Partials/Form/EditableText";

    export default {
        name: "TestEditableText",
        components: {
            EditableText
        },
        data() {
            return {
                text1: "Testtext 1",
                text2: "Testtext 2",
                text3: "Testtext 3"
            };
        }
    }
</script>

<style lang="scss">
    .TestEditableText_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }
</style>
