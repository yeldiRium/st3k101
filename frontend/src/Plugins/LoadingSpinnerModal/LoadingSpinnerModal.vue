<template>
    <modal name="loading"
           :clickToClose="false"
           :width="size"
           :height="size"
    >
        <LoadingSpinner :style="style"/>
    </modal>
</template>

<script>
import LoadingSpinner from "./LoadingSpinner";
import ClosableModal from "../../components/Partials/Modal/ClosableModal";

export default {
  name: "LoadingSpinnerModal",
  extends: ClosableModal,
  components: {
    LoadingSpinner
  },
  props: {
    size: {
      default: "400px"
    }
  },
  computed: {
    style() {
      return {
        width: this.size,
        height: this.size
      };
    }
  },
  methods: {
    close() {
      this.$modal.hide("loading");
    }
  }
};
</script>

<style lang="scss">
</style>
