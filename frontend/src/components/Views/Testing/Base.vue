<template>
    <v-app>
        <v-content>
            <v-container fill-height fluid>
                <div class="centered">
                    <router-view/>
                </div>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
    export default {
        name: "TestingBase"
    };
</script>

<style lang="scss">
    * {
        padding: 0;
        margin: 0;
    }

    .centered {
        margin: auto;
    }
</style>
