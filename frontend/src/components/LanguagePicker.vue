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
                         @click="setLanguage(language)"
            >
                <v-list-tile-title>
                    {{ language.long }}
                </v-list-tile-title>
            </v-list-tile>
        </v-list>
    </v-menu>
</template>

<script>
    import {map} from "ramda";

    import Language from "../api/Model/Language";

    export default {
        created() {
            this.fetchLanguages();
        },
        data() {
            return {
                loading: "loading",
                currentLanguage: {
                    // TODO: read from store
                    short: "de",
                    long: "deutsch"
                },
                languageOptions: []
            }
        },
        methods: {
            /**
             * Fetch the available Languages from the API and parse them to be
             * usable by the dropdown menu.
             */
            fetchLanguages() {
                Language.all().fork(
                    data => {
                        this.loading = "error";
                    },
                    data => {
                        data = map(
                            languageTuple => ({
                                short: languageTuple[0],
                                long: languageTuple[1]
                            }),
                            data
                        );
                        this.loading = "done";
                        this.languageOptions = data;
                    }
                );
            },
            /**
             * Set the global language state to another one.
             *
             * TODO: replace with store action
             */
            setLanguage(language) {
                this.currentLanguage = language;
                console.log(language);
            }
        }
    }
</script>

<style lang="scss">
    .languageMenu {
        max-height: 80%;
    }
</style>
