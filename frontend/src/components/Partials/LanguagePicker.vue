<template>
    <!-- dropdown select box of all languages -->
    <!-- preview with language.long, language.short as value -->
</template>

<script>
    import {mapState, mapMutations} from "vuex";

    export default {
        data() {
            return {
                loading: "loading",
            }
        },
        computed: {
            ...mapState("language", {
                currentLanguage: state => state.currentLanguage,
                languageOptions: state => state.languageOptions
            })
        },
        methods: {
            ...mapMutations("language", [
                "setCurrentLanguage"
            ])
        }
    }
</script>

<style lang="scss">
    .languageMenu {
        max-height: 80%;
    }
</style>
