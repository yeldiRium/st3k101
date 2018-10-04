<template>
    <div class="account">
        <Button @action="logout">
            Logout
        </Button>
        <Button @action="openForgetDataSubject">
            Forget DataSubject
        </Button>
    </div>
</template>

<script>
import { mapGetters } from "vuex-fluture";

import Button from "../../Partials/Form/Button";
import ForgetDataSubject from "../../Partials/Modal/ForgetDataSubject";
import { forgetDataSubject } from "../../../api/DataSubject";

export default {
  name: "Account",
  components: {
    Button
  },
  computed: {
    ...mapGetters("session", ["dataClient", "sessionToken"])
  },
  methods: {
    logout() {
      this.$load(this.$store.dispatch("session/endSession")).fork(
        this.$handleApiError,
        () => this.$router.push({ name: "Authentication" })
      );
    },
    openForgetDataSubject() {
      this.$modal.show("modal-forget-datasubject", {
        handler: this.forgetDataSubject
      });
    },
    forgetDataSubject({ dataSubject }) {
      this.$load(forgetDataSubject(this.sessionToken, dataSubject)).fork(
        this.$handleApiError,
        () => {
          this.$notify({
            type: "warn",
            title: "Personal data was forgotten.",
            text: "Your mind may now rest at ease."
          });
        }
      );
    }
  }
};
</script>

<style lang="scss">
</style>
