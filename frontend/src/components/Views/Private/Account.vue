<template>
    <div class="account">
        <Button @click="logout">
            Logout
        </Button>
    </div>
</template>

<script>
    import {mapGetters} from "vuex";

    import {endSession} from "../../../api2/Authentication";

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
                    endSession(this.sessionToken)
                ).fork(
                    this.$handleApiError,
                    () => this.$router.push({name: "Authentication"})
                )
            }
        }
    }
</script>

<style lang="scss">

</style>
