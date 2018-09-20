<template>
    <nav class="menu-bar-private elevation-8">
        <ul class="menu-bar-private__navigation">
            <li>
                <router-link
                        to="/private/dashboard"
                        class="menu-bar-private__link"
                        tabindex="0"
                >
                    <dashboard-icon class="menu-bar-private__icon"
                                    :style="iconStyle"/>
                </router-link>
            </li>
            <li>
                <router-link
                        to="/private/questionnaires"
                        class="menu-bar-private__link"
                        tabindex="0"
                >
                    <list-icon class="menu-bar-private__icon"
                               :style="iconStyle"/>
                </router-link>
            </li>
            <li>
                <router-link
                        to="/private/account"
                        class="menu-bar-private__link"
                        tabindex="0"
                >
                    <identity-icon class="menu-bar-private__icon"
                                   :style="iconStyle"/>
                </router-link>
            </li>
        </ul>
    </nav>
</template>

<script>
import { mapState } from "vuex-fluture";

import DashboardIcon from "../../../assets/icons/baseline-dashboard-24px.svg";
import ListIcon from "../../../assets/icons/baseline-list-24px.svg";
import IdentityIcon from "../../../assets/icons/baseline-perm_identity-24px.svg";

export default {
  name: "MenuBarPrivate",
  components: {
    DashboardIcon,
    ListIcon,
    IdentityIcon
  },
  computed: {
    ...mapState("global", ["window"]),
    iconStyle() {
      const side = this.window.height / (10 * 24);
      return {
        transform: `scale(${side}, ${side})`,
        margin: `0 ${side * 12}px 0 ${side * 12}px`
      };
    }
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";
@import "../../scss/_elevation";

.menu-bar-private {
  background-color: $verydark;

  &__navigation {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    list-style: none;

    > li {
      display: flex;
      justify-content: center;

      > a {
        display: flex;
        justify-content: center;
        align-content: center;
      }
    }
  }

  &__link {
    height: 100%;

    .menu-bar-private__icon {
      fill: $primary-dark;
    }

    &.router-link-active {
      fill: $primary-light;

      .menu-bar-private__icon {
        fill: $primary-light;
      }
    }
  }
}
</style>
