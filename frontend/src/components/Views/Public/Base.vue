<template>
    <!-- menubar with languagepicker-->
    <!-- content -->
       <router-view :key="$route.fullPath"/>
    <!-- end content -->
</template>

<script>
    import LanguagePicker from "../../Partials/LanguagePicker";

    export default {
        name: "PublicBase",
        components: {LanguagePicker}
    };
</script>

<style lang="scss">
    * {
        padding: 0;
        margin: 0;
    }
</style>
