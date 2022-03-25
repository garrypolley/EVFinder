<template>
  <b-dd id="trim-dd" size="sm" variant="outline-primary" class="px-1">
    <template #button-content>
      {{ filterDisplayName }}
      <span v-if="selectionCount > 0">
        <b-badge variant="success">
          {{ numOfSelections }}
        </b-badge>
      </span>
    </template>

    <b-dropdown-form>
      <b-form-checkbox
        v-for="item in this.filterOptions[inventoryKey]"
        :key=item
        :value="item"
        v-model="localFilterSelections[inventoryKey]"
        name="filterDisplayName | kebabCase"
        class="mb-3"
        >
        {{ item }}
      </b-form-checkbox>
    </b-dropdown-form>
  </b-dd>
</template>

<script>
import { mapActions, mapState } from 'vuex'


export default {
  props: {
    filterDisplayName: {required: true, type: String},
    inventoryKey: {required: true, type: String},
    customFilter: {required: false, type: String},
  },

  data() {
      return {
        /*
        There doesn't seem to be a reasonable way to store form checkbox data in
        a Vuex store. So using a store and forward pattern to address this.
        The form data is initially stored in this local data object, which is
        being watched. When this data object changes, the watcher will commit
        this entire object into the Vuex store.
        */
        localFilterSelections: {
          'dealerNm': [],
          'inventoryStatus': [],
          'trimDesc': [],
          'drivetrainDesc': [],
          'ExtColorLongDesc': [],
          'price': [],
        },

      }
    },  // data
  
  methods: {
      ...mapActions(['updateFilterSelections']),
  },

  computed: {
    // Vuex
    ...mapState([
      'inventory',
      'filterSelections',
      'filterOptions',
      'inventoryCount'
    ]),

    numOfSelections() {
      console.log(this.localFilterSelections)
      console.log(`Selection: ${Object.values(this.localFilterSelections)[0].length}`)
      return Object.values(this.localFilterSelections)[0].length
    },

  },

  watch: {
      // Watching this local data and when it updates, writing the data into the
      // Vuex store
      localFilterSelections: {
        handler: function (val) {
          this.updateFilterSelections(val)
        },
        // The callback will be called whenever any of the watched object properties
        // change regardless of their nested depth
        deep: true
      },
  }, // watch

  filters: {
    kebabCase: function (value) {
      return value.replace(' ', '-')
    },
  }, // filters
}
</script>

<style>

</style>