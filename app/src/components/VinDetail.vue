<template>
  <b-card>
    <b-row class="justify-content-md-center">
      <div v-if="vinTableBusy" class="text-center my-2">
        <b-spinner class="align-middle mr-2" variant="success"></b-spinner>
        <strong>Fetching Details for This Vehicle...</strong>
      </div>
    </b-row>

      <!-- Vin Details List Group -->
      <!-- Dealer Website Button -->
      <div v-if="form.model != 'N'">
        <div v-if="hasHyundaiVinDetail(vinDetail[row.item.vin])">
          <b-row class="py-2" align-h="center">
            <b-button
              size="md"
              variant="light"
              @click="openUrlInNewWindow(vinDetail[row.item.vin]['DI']['DealerVDPURL'])"
              class="mr-2 align-middle"
              >
              Dealer's Website for This Vehicle
              <b-icon icon="box-arrow-up-right" aria-hidden="true" class="ml-2" font-scale="1"></b-icon>
            </b-button>
          </b-row>
        </div>
      </div>
      <!-- Window sticker for Kias -->
      <!-- <div v-if="form.model == 'N'">
          <b-row class="py-2" align-h="center">
            <b-button
              size="md"
              variant="light"
              @click="openUrlInNewWindow('https://www.kia.com/us/services/us/windowsticker/load/' + row.item.vin)"
              class="mr-2 align-middle"
              >
              Window Sticker for This Vehicle
              <b-icon icon="box-arrow-up-right" aria-hidden="true" class="ml-2" shift-v="5" font-scale=".8"></b-icon>
            </b-button>
          </b-row>
      </div> -->
      
        <b-list-group
          horizontal
          v-for="(item, key) in vinDetail[row.item.vin]" :key=key
        >
        <!-- We're displaying the Dealer URL above, don't display it here -->
          <b-col cols=4 v-if="key != 'DI'">
            <b-list-group-item class="border-0 py-1"><b>{{ key }}</b></b-list-group-item>
          </b-col>
          <div v-if="key != 'DI'">
            <b-list-group-item class="border-0 py-1">{{ item }}</b-list-group-item>
          </div>
        
      </b-list-group>
      
  
    <b-button size="sm" @click="row.toggleDetails" variant="light">Hide Details</b-button>
  </b-card>
</template>

<script>
  import {mapState} from 'vuex'
  import {has} from 'lodash'

export default {
  mounted() {},

  data() {
      return {
        vinDetail: {},
        vinTableBusy: false,
        vinDetailClickedCount: 0,
      }
  },

  computed: {
      ...mapState([
        // 'tableBusy',
        // 'inventory',
        // 'filterSelections',
        'form',
        'vinTableBusy'
      ]),
  },

  methods: {
    hasHyundaiVinDetail(item) {
      return (has(item, 'DI') && has(item['DI'], 'DealerVDPURL'))
    },
  },

}  // default
</script>

<style>

</style>