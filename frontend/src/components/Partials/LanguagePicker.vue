<template>
    <v-menu offset-y
            allow-overflow
            lazy
            content-class="languageMenu"
            transition="slide-y-reverse-transition"
    >
        <v-btn flat
               slot="activator"
        >
            {{ currentLanguage.long }}
        </v-btn>
        <v-list>
            <v-list-tile v-for="language in languageOptions"
                         :key="language.short"
                         @click="setCurrentLanguage(language)"
            >
                <v-list-tile-title>
                    {{ language.long }}
                </v-list-tile-title>
            </v-list-tile>
        </v-list>
    </v-menu>
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
