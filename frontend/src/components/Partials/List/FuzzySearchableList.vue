<template>
    <div class="container"
    >
        <label>
            Search:
            <input class="search"
                   type="text"
                   v-model="searchString"
            />
        </label>
        <table cellpadding="0"
               cellspacing="0"
        >
            <thead class="table-header">
                <tr>
                    <th class="table-header__column"
                        v-for="key in [...keys, ...displayOnlyKeys]"
                        :key="key.key"
                    >
                        {{ key.display }}
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-row"
                    v-for="item in matchingItems"
                    @click="clicked(item)"
                >
                    <td v-for="key in keys">
                        <p :class="{'highlighted': item.matches.hasOwnProperty(key.key) && !(searchString.length === 0) }">
                            {{ item.item[key.key] }}
                        </p>
                    </td>
                    <td v-for="key in displayOnlyKeys">
                        {{ item.item[key.key] }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import * as R from "ramda";

export default {
  name: "FuzzySearchableList",
  props: {
    items: {
      type: Array,
      default: () => []
    },
    keys: {
      type: Array,
      default: () => []
    },
    displayOnlyKeys: {
      type: Array,
      default: () => []
    },
    itemKey: {
      type: String,
      default: "id"
    },
    orderBy: {
      type: String
    }
  },
  data() {
    return {
      searchString: ""
    };
  },
  computed: {
    matchingItems() {
      if (R.isNil(this.items)) {
        return [];
      }
      return R.sortBy(
        item => item.item[this.sortBy],
        R.filter(
          x => !R.isEmpty(x.matches),
          R.map(item => {
            return { item, matches: this.getMatchingKeys(item) };
          }, this.items)
        )
      );
    },
    searchRegExp() {
      return RegExp(
        R.pipe(
          R.split(" "),
          R.intersperse(".*"),
          R.join("")
        )(this.searchString.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
        "i"
      );
    },
    sortBy() {
      return R.isNil(this.orderBy) ? this.keys[0].key : this.orderBy;
    }
  },
  methods: {
    getMatchingKeys(item) {
      let matches = {};
      for (let key of this.keys) {
        key = key.key; // kiki, do you love me? are your riding?
        if (!item.hasOwnProperty(key)) {
          continue;
        }
        let value = item[key];
        if (typeof value !== "string") {
          value = JSON.stringify(value);
        }
        let match = this.searchRegExp.exec(value);
        if (!R.isNil(match)) {
          matches[key] = match[0];
        }
      }
      return matches;
    },
    clicked(item) {
      this.$emit("item-clicked", item.item);
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../scss/_variables.scss";

.container {
  width: 100%;
}

label {
  width: 100%;
}

table {
  width: 100%;
}

.highlighted {
  border: 1px solid $primary;
  border-radius: 7px;
  box-shadow: 0 0 10px $primary;
}

th,
td {
  padding: 0.3em 1em 0.3em 1em;
  border-bottom: $primary-light 1px solid;
}

.table-header {
  &__column {
    border-bottom: $primary 3px solid;
  }
}

.table-row:hover {
  background-color: $primary-light;
}

p {
  padding: 0.1em;
}
</style>
