<template>
    <div id="private-base">
        <MenuBarPrivate/>

        <div class="content">
            <router-view />
        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex";

    import LanguagePicker from "../../Partials/LanguagePicker";
    import MenuBarPrivate from "../../Partials/Menu/MenuBarPrivate"

    export default {
        components: {LanguagePicker, MenuBarPrivate},
        name: "App",
        created() {
            if (!this.isLoggedIn) {
                this.$router.replace({
                    name: "Authentication"
                })
            }
        },
        computed: {
            ...mapState("session", ["isLoggedIn"])
        }
    };
</script>

<style lang="scss">
    @import "../../scss/_variables.scss";
    @import "../../scss/_elevation.scss";

    * {
        padding: 0;
        margin: 0;
    }

    #private-base {
        position: absolute;
        height: 100%;
        width: 100%;

        display: grid;
        grid-template-areas:
            "content"
            "menubar";
        grid-template-rows: auto 15%;
    }

    .content {
        grid-area: content;

        overflow-y: scroll;
    }

    .menu-bar-private {
        grid-area: menubar;
    }
</style>
