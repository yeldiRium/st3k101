<template>
    <div class="btn-group language_menu">
        <v-select
                :items="languageOptions"
                v-model="currentLanguage"
                label="Language"
                single-line
                item-text="long"
                item-value="short"
                return-object
        ></v-select>
        <!--
        TODO: make this look less shitty. position it centered vertically
         -->
    </div>
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
            persistLanguageChange(language) {
                console.log(language);
            }
        },
        watch: {
            /**
             * When the selected language changes, call the persist method to
             * update the global state.
             *
             * @param newVal
             * @param oldVal
             */
            currentLanguage(newVal, oldVal) {
                this.persistLanguageChange(newVal);
            }
        }
    }
</script>

<style lang="scss">

</style>
