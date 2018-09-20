<template>
    <div class="account">
        <Button @action="logout">
            Logout
        </Button>
    </div>
</template>

<script>
import { mapGetters } from "vuex-fluture";

import Button from "../../Partials/Form/Button";

export default {
  name: "Account",
  components: {
    Button
  },
  computed: {
    ...mapGetters("session", ["dataClient"])
  },
  methods: {
    logout() {
      this.$load(this.$store.dispatch("session/endSession")).fork(
        this.$handleApiError,
        () => this.$router.push({ name: "Authentication" })
      );
    }
  }
};
</script>

<style lang="scss">
</style>
