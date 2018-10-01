<template>
    <div class="container">
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
                        v-for="key in keys"
                        :key="key.key"
                    >
                        {{ key.name }}
                    </th>
                </tr>
            </thead>
            <tbody> <!-- todo set height with cimputed classes -->
                <tr class="table-row"
                    v-for="item in matchingItems"
                    @click="clicked(item)"
                >
                    <td v-for="key in keys">
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
    itemKey: {
      type: String,
      default: "id"
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
      return R.filter(
        x => !R.isEmpty(x.matches),
        R.map(item => {
          return { item, matches: this.getMatchingKeys(item) };
        }, this.items)
      );
    },
    searchRegExp() {
      return RegExp(
        R.pipe(
          R.split(" "),
          R.intersperse(".*"),
          R.join("")
        )(this.searchString),
        "i"
      );
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

table {
  width: 100%;
}

th,
td {
  padding: 0.3em 1em 0.3em 1em;
  border-bottom: $primary-light 1px solid;
}

.table-header {
  &__column {
    border-bottom: $primary-light 3px solid;
  }
}

.table-row:hover {
  background-color: $primary-light;
}

tbody {
  display: block;
  overflow-y: scroll;
  overflow-x: hidden;
}
thead,
tbody tr {
  display: table;
  width: 100%;
  table-layout: fixed;
}
thead {
  width: calc(100% - 1em);
}
</style>
