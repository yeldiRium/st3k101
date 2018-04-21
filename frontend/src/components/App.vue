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
                <v-toolbar-side-icon @click.stop="searchBar = true">
                    <v-icon>search</v-icon>
                </v-toolbar-side-icon>
            </v-toolbar>
            <v-toolbar
                    v-else
                    app
                    fixed
                    clipped-left
                    color="white">
                <v-toolbar-side-icon @click.stop="searchBar = false">
                    <v-icon color="black">close</v-icon>
                </v-toolbar-side-icon>
                <v-text-field
                        light
                        solo
                        placeholder="Type keyword..."
                        v-show="searchBar"
                        class="elevation-0"/>
                <v-toolbar-side-icon @click.stop="searchBar = false">
                    <v-icon color="black">search</v-icon>
                </v-toolbar-side-icon>
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
    export default {
        name: "App",
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
        }),
        props: {},
        created() {
        }
    };
</script>

<style lang="scss">
    * {
        padding: 0;
        margin: 0;
    }
</style>
