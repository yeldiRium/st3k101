<template>
    <div class="account">
        <Button @click="logout">
            Logout
        </Button>
    </div>
</template>

<script>
    import {mapGetters} from "vuex-fluture";

    import {endSession} from "../../../api/Authentication";

    import Button from "../../Partials/Form/Button";

    export default {
        name: "Account",
        components: {
            Button
        },
        computad: {
            ...mapGetters("session", ["sessionToken"])
        },
        methods: {
            logout() {
                this.$load(
                    this.$store.dispatch("session/endSession")
                )
                    .fork(
                        this.$handleApiError,
                        () => this.$router.push({name: "Authentication"})
                    );
            }
        }
    }
</script>

<style lang="scss">

</style>
