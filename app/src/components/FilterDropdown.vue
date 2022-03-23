<template>
  <b-dd id="trim-dd" size="sm" variant="outline-primary" class="px-1">
          <template #button-content>
            {{ filterDisplayName }}
            <span v-if="localFilterSelections.trimDesc.length > 0">
              <b-badge variant="success">
                {{ localFilterSelections.trimDesc.length }}
              </b-badge>
            </span>
          </template>

          <b-dropdown-form>
            <b-form-checkbox
              v-for="item in this.filterOptions.trimDesc" :key=item
              :value="item"
              v-model="localFilterSelections.trimDesc"
              name="trim-description"
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
    inventoryKey: {required: true, type: String}
  },
}
</script>

<style>

</style>