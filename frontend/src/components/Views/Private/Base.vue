<template>
    <v-app id="inspire" dark>
        <v-navigation-drawer
                clipped
                fixed
                v-model="drawer"
                app
        >
            <v-list dense>
                <v-list-tile v-for="item in navigationItems"
                             :key="item.name"
                             router
                             exact
                             :to="{ name: item.action, params: item.payload }">
                    <v-list-tile-action>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ item.text }}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
        </v-navigation-drawer>
        <transition transition-mode="out-in">
            <v-toolbar
                    v-if="!searchBar"
                    app
                    fixed
                    clipped-left>
                <v-toolbar-side-icon
                        @click.stop="drawer = !drawer"/>
                <v-toolbar-title>Trashbin</v-toolbar-title>
                <v-spacer/>
                <language-picker />
            </v-toolbar>
        </transition>
        <v-content>
            <v-container fluid fill-height>
                <router-view/>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
    import LanguagePicker from "../../Partials/LanguagePicker";

    export default {
        components: {LanguagePicker},
        name: "App",
        created() {
            if (!this.$store.getters["session/isLoggedIn"]) {
                this.$router.replace({
                    name: "PublicBase"
                })
            }
        },
        data: () => ({
            drawer: true,
            searchBar: false,
            navigationItems: [
                {
                    action: "Dashboard",
                    icon: "dashboard",
                    text: "Dashboard"
                },
                {
                    action: "SurveyForSubmission",
                    icon: "image",
                    text: "Survey",
                    payload: {
                        id: "blub"
                    }
                }
            ]
        })
    };
</script>

<style lang="scss">
    * {
        padding: 0;
        margin: 0;
    }
</style>
