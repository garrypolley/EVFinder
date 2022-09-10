import requests

from flask import Blueprint, request

from libs.libs import send_response, send_error_response, validate_request

ford = Blueprint(name="ford", import_name=__name__)

# s = requests.Session()
api_url = 'https://shop.ford.com/aemservices/cache/inventory/dealer/dealers' #?make=Ford&market=US&inventoryType=Radius&maxDealerCount=10&model=mache&segment=Crossover&zipcode=90210'

@ford.route('/api/inventory/ford', methods=['GET'])
def get_ford_inventory():
  request_args = request.args

  zip_code = request_args['zip']
  year = request_args['year']
  model = request_args['model']
  radius = request_args['radius']

  with requests.Session() as s:
      # The Ford inventory API URL requires a 'dealerSlug', which is obtained by first making a call to a dealers endpoint, and a subsequent call to the dealer-lot endpoint which contains the available inventory
    
        # s.headers = headers
        s.timeout = 15  # Both connect and read timeout
        s.params = {
          'make': 'Ford',
          'market': 'US',
          'inventoryType': 'Radius',
          'maxDealerCount': '1',
          'model': model,
          'segment': 'Crossover',
          'zipcode': zip_code
        }

    
        dealer_lookup = s.get(
          f'https://shop.ford.com/aemservices/cache/inventory/dealer/dealers',
        ).json()

        try:
          dealer_lookup['status']
          if 'success' in dealer_lookup['status']:
            dealer_slug = dealer_lookup['data']['firstFDDealerSlug']

            inventory = s.get(
              f'https://shop.ford.com/aemservices/cache/inventory/dealer-lot',
              params={'dealerSlug': dealer_slug}
            )
            return send_response(
              response_data = inventory.json(),
              content_type='application/json',
              cache_control_age=3600
            )
          elif 'error' in dealer_lookup['status']:
            return send_error_response(
              error_message=dealer_lookup['errorMessage'],
              error_data=s.url,
              status_code=500
            )
        except KeyError:
          print(f'ERROR Here: {inventory}')
          error_message = 'An error occurred with the ford API'
          return send_error_response(
            error_message=error_message,
            error_data=inventory
      )
  # Request could not be validated
        else:
          return send_error_response(
            error_message='Request could not be validated',
            error_data=request.url,
            status_code=400
            )

@ford.route('/api/vin/ford', methods=['GET'])
def get_vin_details():
  request_args = request.args

  zip_code = request_args['zip']
  vin = request_args['vin']

  # We'll use the requesting UA to make the request to the ford APIs
  user_agent = request.headers['User-Agent']
  
  headers = {
      'User-Agent': user_agent,
      'referer': 'https://www.vw.com/'
  }
  
  vin_post_data = {
    "operationName": "VehicleData",
    "variables": {
      "vin": vin,
      "zipcode": zip_code
    },
    'query': 'query VehicleData($vin: String, $zipcode: String) {vehicle: getVehicleByVinAndZip(vin: $vin, zipcode: $zipcode) { portInstalledOptions vin model modelCode modelYear modelVersion carlineKey msrp mpgCity subTrimLevel engineDescription exteriorColorDescription exteriorColorBaseColor exteriorColorCode exteriorSwatchUrl interiorColorDescription interiorColorBaseColor interiorColorCode interiorSwatchUrl mpgHighway trimLevel mediaImageUrl mediaImageUrlAlt mediaAssets {   description   type   asset   __typename } onlineSalesURL dealerEnrollmentStatusInd highlightFeatures {   key   title   __typename } factoryModelYear dealerInstalledAccessories {   mdmCode   title   longTitle   description   image   itemPrice   creativeTitle   __typename } dealer {   generatedDate   dealerid   name   dealername   seolookupkey   address1   address2   city   state   postalcode   country   url   phone   latlong   staticMapsUrl   distance   inventoryCount   aor   isSatellite   isAssessing   lmaId   __typename } specifications {   text   values {     key     label     longTitle     value     __typename   }   key   __typename } destinationCharge __typename}}'
  }
  
  vin_detail = requests.post(
      url=api_url,
      headers=headers,
      json=vin_post_data,
      verify=False
    )
    
  data = vin_detail.json()

  if len(data['data']['vehicle']) > 0:
    return send_response(
      response_data=data,
      content_type='application/json',
      cache_control_age=3600
    )
  else:
    error_message = 'An error occurred with the ford API'
    return send_error_response(
      error_message=error_message,
      error_data=data
    )