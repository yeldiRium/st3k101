
<template>
    <div id="private-base">
        <MenuBarPrivate/>

        <div class="content">
            <router-view :key="$route.fullPath"/>
        </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex-fluture";

import LanguagePicker from "../../Partials/LanguagePicker";
import MenuBarPrivate from "../../Partials/Menu/MenuBarPrivate";

export default {
  components: { LanguagePicker, MenuBarPrivate },
  name: "App",
  watch: {
    isLoggedIn: {
      immediate: true,
      handler(isLoggedIn) {
        if (!isLoggedIn) {
          this.$router.replace({
            name: "Authentication"
          });
        } else {
          this.loadMyQuestionnaires()
            .chain(this.loadMyTrackerEntries)
            .fork(this.$handleApiError, () => {});
        }
      }
    }
  },
  computed: {
    ...mapGetters("session", ["isLoggedIn"])
  },
  methods: {
    loadMyQuestionnaires() {
      return this.$store.dispatch("questionnaires/loadMyQuestionnaires");
    },
    loadMyTrackerEntries() {
      return this.$store.dispatch("trackerEntries/loadMyTrackerEntries");
    }
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
  grid-template-areas: "content" "menubar";
  grid-template-rows: auto 10%;
}

.content {
  grid-area: content;

  overflow-y: scroll;
}

.menu-bar-private {
  grid-area: menubar;
}
</style>
