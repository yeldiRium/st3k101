<template>
    <v-app>
        <v-toolbar
                app
                fixed
                clipped-left>
            <v-toolbar-title>Trashbin</v-toolbar-title>
            <v-spacer/>
            <language-picker />
        </v-toolbar>
        <v-content>
            <v-container fill-height>
                <router-view/>
            </v-container>
        </v-content>
    </v-app>
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
