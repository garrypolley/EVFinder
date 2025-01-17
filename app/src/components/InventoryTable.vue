<template>
  <b-container>
    <!-- Let's filter -->
    <Filters/>

    <!-- Table here -->
    <b-row class="d-flex justify-content-center">
      <!-- The API returned an error, so display an error message -->
      <div v-if="this.apiErrorDetail.length > 0">
        <ErrorMessage/>
      </div>
      <div v-else-if="showInventoryAlert" class="mt-5">
        <b-alert show variant="success" class="no-inventory px-5">
          No Vehicles Were Found. Adjust your search parameters and try again.
        </b-alert>
      </div>
      <div v-else>
        <b-table
          hover
          stacked="sm"
          responsive
          :busy="tableBusy"
          :items="this.inventory"
          :fields="this.fields"
          :sort-compare="customSort"
          :filter="this.filterSelections"
          @row-clicked="toggleDetails"
          @filtered="onFiltered"
          :filter-function="filterFunction"
          >

          <!-- Exterior Color -->
          <template #cell(exterior-color)="data">
            {{ titleCase(data.item.ExtColorLongDesc) }}
          </template>

          <!-- Interior Color -->
          <template #cell(interior-color)="data">
            {{ data.item.interiorColorCd }}
          </template>
          
          <!-- Dealer Information for Mobile Devices. Displays dealer name only-->
          <template #cell(dealer-name-only)="data">
            <b-link
              :href="`https://${data.item.dealerUrl}`"
              target="_blank"
              >
                {{ data.item.dealerName }}
              </b-link>
          </template>

          <!-- Dealer Information for Large Screen Devices.
          Displays Dealer Name - City, State -->
          <template #cell(dealer-name-address)="data">
            <b-link
              :href="`https://${data.item.dealerUrl}`"
              target="_blank"
              >
                {{ data.item.dealerName }}
              </b-link>
          </template>

          <!-- Distance -->
          <template #cell(distance)="data">
            {{ data.item.distance }} mi.
          </template>

          <!-- VIN Column -->
          <template #cell(vin-with-more-details)="row">
            <!-- If we've already made the API call and stored the VIN data, just show it -->
            <div v-if="row.item.vin in vinDetail">
              <b-button size="sm" variant="light" @click="row.toggleDetails" class="mr-2 align-middle vin">
                {{ row.item.vin }} <b-icon-chevron-down aria-hidden="true"></b-icon-chevron-down>
              </b-button>
            </div>
            <!-- Otherwise, make the VIN data API call -->
            <div v-else>
              <b-button size="sm" variant="light" @click="toggleDetails(row.item)" class="mr-2 align-middle vin">
                {{ row.item.vin }} <b-icon-chevron-down aria-hidden="true"></b-icon-chevron-down>
              </b-button>
            </div>
          </template>

          <!-- Vin Details Section -->
          <template #row-details="row">
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
                      <b-icon-box-arrow-up-right aria-hidden="true" class="ml-2" font-scale="1"></b-icon-box-arrow-up-right>
                    </b-button>
                  </b-row>
                </div>
              </div>
              <!-- Window sticker for Genesis -->
              <div v-if="form.model == 'GV60'">
                  <b-row class="py-2" align-h="center">
                    <b-button
                      size="md"
                      variant="light"
                      @click="openUrlInNewWindow(generateGenesisWindowStickerUrl(row.item.vin, form.model))"
                      class="mr-2 align-middle"
                      >
                      Window Sticker for This Vehicle
                      <b-icon-box-arrow-up-right aria-hidden="true" class="ml-2" shift-v="5" font-scale=".8"></b-icon-box-arrow-up-right>
                    </b-button>
                  </b-row>
              </div>
              <!-- Direct Dealer URL for Volkswagen -->
              <div v-if="form.model == 'ID.4' && row.item.onlineSalesURL != ''">
                  <b-row class="py-2" align-h="center">
                    <b-button
                      size="md"
                      variant="light"
                      @click="openUrlInNewWindow(row.item.onlineSalesURL)"
                      class="mr-2 align-middle"
                      >
                      Dealer's Website for This Vehicle
                      <b-icon-box-arrow-up-right aria-hidden="true" class="ml-2" shift-v="5" font-scale=".8"></b-icon-box-arrow-up-right>
                    </b-button>
                  </b-row>
              </div>
              
                <b-list-group
                  horizontal
                  v-for="(item, key) in vinDetail[row.item.vin]" :key=key
                >
                <!-- We're displaying the Dealer URL above, don't display it here -->
                  <b-col cols=8 md=4 v-if="key != 'DI'">
                    <b-list-group-item class="border-0 py-1"><b>{{ key }}</b></b-list-group-item>
                  </b-col>
                  <div v-if="key != 'DI'">
                    <b-list-group-item class="border-0 py-1">{{ item }}</b-list-group-item>
                  </div>
              </b-list-group>
              
          
            <b-button size="sm" @click="row.toggleDetails" variant="light">Hide Details</b-button>
          </b-card>
        </template>
              <!-- Table Busy Indicator -->
              <template #table-busy>
                <div class="text-center my-2">
                  <b-spinner class="align-middle mr-2" variant="success"></b-spinner>
                  <strong>Fetching Vehicle Inventory...</strong>
                </div>
            </template>
          </b-table>
      </div>
    </b-row>
  </b-container>
</template>

<script>
  import ErrorMessage from './ErrorMessage.vue'
  import Filters from './Filters.vue'

  import { mapActions, mapState } from 'vuex'
  import { has } from 'lodash'

  import { convertToCurrency } from '../libs'
  
  import { getHyundaiVinDetail } from '../manufacturers/hyundai'
  import { getKiaVinDetail } from '../manufacturers/kia'
  import { getGenesisVinDetail } from '../manufacturers/genesis'
  import { getVolkswagenVinDetail } from '../manufacturers/volkswagen'
  
  export default {
    components: {
      ErrorMessage,
      Filters
      },

      created() {
        window.addEventListener('beforeunload', this.beforeWindowUnload)
      },

      mounted() {
      },

      beforeDestroy() {
        window.removeEventListener('beforeunload', this.beforeWindowUnload)
      },

    data() {
      return {
        vinDetail: {},
        vinTableBusy: false,

        fields: [
          { key: 'exteriorColor', label: 'Ext. Color', sortable: true, sortDirection: 'desc'},
          { key: 'interiorColor', label: 'Int. Color', sortable: true, sortDirection: 'desc'},
          { key: 'trimDesc', label: 'Trim', sortable: true, sortDirection: 'desc'},
          { key: 'drivetrainDesc', label: 'Drivetrain', sortable: true, sortDirection: 'desc'},
          { key: 'price', label: 'MSRP', sortable: true, sortDirection: 'desc', formatter: convertToCurrency},
          { key: 'deliveryDate', label: 'Delivery Date', formatter: "formatDate", sortable: true, sortByFormatted: true, filterByFormatted: true },

          // Display the Dealer's name - city, state on large-screen devices (hidden on mobile, iPad portrait, etc)
          { key: 'dealer-name-address', label: 'Dealer', sortable: true, sortByFormatted: true, filterByFormatted: true, class: "d-none d-lg-table-cell"},

          // Display only the Dealer's name on mobile devices (hidden on desktop, iPad landscape, etc)
          { key: 'dealer-name-only', label: 'Dealer', sortable: true, sortByFormatted: true, filterByFormatted: true, class: "d-lg-none" },
          
          // Only show the Distance column on large+ devices (hidden on mobile, iPad portrait, etc)
          { key: 'distance', label: 'Distance', sortable: true, sortDirection: 'desc', class: 'd-none d-lg-table-cell'},
          { key: 'vin-with-more-details', label: "VIN", sortable: false }
        ],
      } // End of return
    },
    methods: {
      ...mapActions([
        'updateStore'
        ]),

      async toggleDetails(item) {
        // Inject _showDetails into the row items. Vue expects this to be present
        // to know this row has additional detail to display upon click
        if (item["_showDetails"]) item["_showDetails"] = false;
        else this.$set(item, "_showDetails", true);

        if (this.form.manufacturer.toLowerCase() === "kia") {
          const kiaVinData = getKiaVinDetail(item)
          this.$set(
            this.vinDetail,  // Where to store
            item.vin,        // What's the key
            kiaVinData,            // Data to store
            )
        }
        else if (this.form.manufacturer.toLowerCase() === "hyundai") {  // Make a vin API call for Hyundai
          // Show users that we're fetching data
          this.vinTableBusy = true
          const hyundaiVinData = await getHyundaiVinDetail(item.vin, this.form.model, this.form.year)
          // Store a new record for each VIN we fetch.
          // this.$set is needed to enable reactive properties on an existing object
          // without this.$set, the nested table will not auto-refresh with this info
          this.$set(
            this.vinDetail,
            item.vin,
            hyundaiVinData
            )
        }
        else if (this.form.manufacturer.toLowerCase() === "genesis") {
          const genesisVinData = getGenesisVinDetail(item)
          this.$set(
            this.vinDetail,  // Where to store
            item.vin,        // What's the key
            genesisVinData,            // Data to store
            )
        }
        else if (this.form.manufacturer.toLowerCase() === "volkswagen") {  // Make a vin API call for Volkswagen
          // Show users that we're fetching data
          this.vinTableBusy = true
          const volkswagenVinData = await getVolkswagenVinDetail(this.form.zipcode, item.vin)
          // Store a new record for each VIN we fetch.
          // this.$set is needed to enable reactive properties on an existing object
          // without this.$set, the nested table will not auto-refresh with this info
          this.$set(
            this.vinDetail,
            item.vin,
            volkswagenVinData
            )
        }

        // Remove the table busy indicator
        this.vinTableBusy = false
      },
      
      priceStringToNumber(priceString) {
        return Number(parseFloat(priceString.replace('$', '').replace(',', '')))
      },

      formatDate(isoDate) {
        if (isoDate) {  // Checking for null values
          // Parsing the ISO8601 isoDate into a DateString (Mon Jan 01 1970) and
          // stripping the leading day of week resulting in Jan 01 1970
          const d = new Date(isoDate).toDateString()
          if (d != 'Invalid Date') {
            return d.substring(4,)
          } else {
              return isoDate
            }
        }
        return ''
      },

      customSort(a, b, key) {
        /*
         Only apply this custom sort to date columns
         Return either
         -1 for a[key] < b[key]
          0 for a[key] === b[key]
          1  for a[key] > b[key].
        */
        if (key == 'PlannedDeliveryDate') {
          const _a = new Date(a[key])  // New Date object
          const _b = new Date(b[key])
          const aDate = Date.parse(_a)  // Convert Date object to epoch
          const bDate = Date.parse(_b)
          
          // Some manufacturers don't include a delivery date in their API response
          // If that's true, fall back to the buit-in sort-compare routine
          if ((_a || _b) == 'Invalid Date') {
            return false
          }

          if (aDate < bDate ){
            return -1
          } 
          else if (aDate === bDate) {
            return 0
          }
          else {
            return 1
          }
        }
        // Fall back to the built-in sort-compare routine for all other keys
        return false
      },

      onFiltered(filteredItems) {
        // Updating the "$num Vehicles Found" text due to filtering
        this.updateStore({'inventoryCount': filteredItems.length})
      },

      openUrlInNewWindow(url) {
        // Fire event to Plausible
        this.$plausible.trackEvent(
          'Outbound Link: Click', {props: {url: url}}
          )

        window.open(url, '_blank')
      },

      filterFunction(rowRecord, filterSelections) {
        // selectedCategories looks like ['trimDesc', ['LIMITED', 'SEL']]
        var selectedCategories = Object.entries(filterSelections).filter(f => f[1].length > 0)
        var selectedCategoriesCount = selectedCategories.length
        var isMatch = []
        
        if (selectedCategoriesCount == 0) {
          // No filters are selected
          return true
        }

        else if (selectedCategoriesCount == 1) {
          // Multiple selections in a single category
          if (selectedCategories[0][0] == 'price') {
            let selectedPrice = selectedCategories[0][1]
            return this.filterByPrice(rowRecord, selectedPrice)
          }
          else {
            return (selectedCategories[0][1].some(val => Object.values(rowRecord).includes(val)))
          }
        }

        else if (selectedCategoriesCount > 1) {
          // One or more selections across multiple categories
         for (var item of selectedCategories) {
           var category = item[0]
           var selectedItems = item[1]

          if (category == 'price') {
            isMatch.push(this.filterByPrice(rowRecord, selectedItems[0]))
          }
          else {
            // Each loop is a category. Do we have an OR match for the selected filter items?
            // e.g. Blue OR Black OR White
            isMatch.push(selectedItems.some(s => Object.values(rowRecord).includes(s)))
            }
          }
         
         if (isMatch.includes(false)) {
           return false
         } else {
           return true
         } 
        }
      },

      filterByPrice(rowRecord, selectedPrice) {
        return this.priceStringToNumber(rowRecord.price) < selectedPrice
      },

      hasHyundaiVinDetail(item) {
        return (has(item, 'DI') && has(item['DI'], 'DealerVDPURL'))
      },

      generateGenesisWindowStickerUrl(vin, genesisModel) {
        const refreshToken = new Date().toISOString().split('T')[0] // 2022-08-01
        return `https://www.genesis.com/us/en/services/windowsticker?refreshToken=${refreshToken}&vehicleType=new&VIN=${vin}&vehicleModel=${genesisModel}`
      },
    }, // methods
    
    computed: {
      ...mapState([
        'apiErrorDetail',
        'tableBusy',
        'inventory',
        'filterSelections',
        'form'
      ]),

      showInventoryAlert() {
        if (
          !this.tableBusy
          && Object.values(this.inventory).length == 0
          && Object.values(this.form).filter(f => f.length > 0).length == Object.keys(this.form).length){
          return true
        }
        else {
          return false
        }
      },
    },  // computed
    watch: {},
  }  // End of default
</script>

<style lang="scss">
  @import '../assets/app_style.scss';

  table.b-table[aria-busy='true'] {
    opacity: 0.6;
  }

  .table-striped tbody tr:nth-of-type(odd) {
    background-color: #F5FFEB !important;
  }

  .table-hover tbody tr:hover {
    background-color: $highlight-bluegreen !important;
}

  .vin {
    font-family: $font-family-monospace;
    font-size: 1rem !important;
    letter-spacing: -.03rem;
}

  .no-inventory {
    color: #6c757d !important;
    font-size: 1.2rem;
    text-align: center;
  }  
</style>