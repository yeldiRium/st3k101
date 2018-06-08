<template>
    <nav class="menubar-container elevation-8">
        <ul class="menubar-navigation">
            <li>
                <router-link to="/private/dashboard" class="menubar-link">
                    <dashboard-icon class="menubar-icon" :style="iconStyle"/>
                </router-link>
            </li>
            <li>
                <router-link to="/private/questionnaires" class="menubar-link">
                    <list-icon class="menubar-icon" :style="iconStyle"/>
                </router-link>
            </li>
            <li>
                <router-link to="/private/account" class="menubar-link">
                    <identity-icon class="menubar-icon" :style="iconStyle"/>
                </router-link>
            </li>
        </ul>
    </nav>
</template>

<script>
    import {mapState} from "vuex";

    import DashboardIcon from "../../../assets/icons/baseline-dashboard-24px.svg";
    import ListIcon from "../../../assets/icons/baseline-list-24px.svg";
    import IdentityIcon from "../../../assets/icons/baseline-perm_identity-24px.svg";

    export default {
        name: "PrivateMenuBar",
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
                }
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";
    @import "../../scss/_elevation";

    .menubar-container {
        background-color: $verydark;
    }

    .menubar-navigation {
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

    .menubar-link {
        height: 100%;

        .menubar-icon {
            fill: $primary-dark;
        }


        &.router-link-active {
            fill: $primary-light;

            .menubar-icon {
                fill: $primary-light;
            }
        }
    }
</style>