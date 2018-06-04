<template>
    <!-- menu bar -->
    <!-- content -->
        <router-view/>
    <!-- content end -->
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
