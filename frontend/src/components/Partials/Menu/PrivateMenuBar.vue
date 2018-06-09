<template>
    <nav class="privatemenubar elevation-8">
        <ul class="privatemenubar-navigation">
            <li>
                <router-link to="/private/dashboard"
                             class="privatemenubar-link">
                    <dashboard-icon class="privatemenubar-icon"
                                    :style="iconStyle"/>
                </router-link>
            </li>
            <li>
                <router-link to="/private/questionnaires"
                             class="privatemenubar-link">
                    <list-icon class="privatemenubar-icon" :style="iconStyle"/>
                </router-link>
            </li>
            <li>
                <router-link to="/private/account" class="privatemenubar-link">
                    <identity-icon class="privatemenubar-icon"
                                   :style="iconStyle"/>
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

    .privatemenubar {
        background-color: $verydark;

        &-navigation {
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

        &-link {
            height: 100%;

            .privatemenubar-icon {
                fill: $primary-dark;
            }

            &.router-link-active {
                fill: $primary-light;

                .privatemenubar-icon {
                    fill: $primary-light;
                }
            }
        }
    }
</style>