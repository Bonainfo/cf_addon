module name : Mobikul: Mobile App Builder
technical name : mobikul

## [1.0.1] - 2017-10-06
### Added
-
### Changed
- "/mobikul/paymentAcquirers" -> when no payment methods present success change to False
- version from 1.0 to 1.0.1
### Removed
-
### Fix
-

## [1.0.2] - 2017-10-06
### Added
-
### Changed
- social login paid changes
- oauth field changes to readonly
- version from 1.0.1 to 1.0.2
### Removed
- remove scoial login section from index.html
### Fix
-

## [1.0.3] - 2017-10-06
### Added
-
### Changed
- state_id and country_id change to state and country in seller profile
- version from 1.0.2 to 1.0.3
### Removed
- remove scoial login section from index.html
### Fix
-


## [1.0.4] - 2017-10-12
### Added
-
### Changed
- in product template api send seller_info = null
- version from 1.0.3 to 1.0.4
### Removed
-
### Fix
-

## [1.0.5] - 2017-10-13
### Added
-
### Changed
- view all sellers product add comment below the seller profile.
- version from 1.0.4 to 1.0.5
### Removed
-
### Fix
- At seller profile info listed review count is 2
- At seller profile info total listed seller product count is 5


## [1.0.6] - 2017-10-13
### Added
- Implement the featured category Url in homepage api
### Changed
- version from 1.0.5 to 1.0.6
### Removed
-
### Fix
-


## [1.0.7] - 2017-10-13
### Added
-
### Changed
- version from 1.0.6 to 1.0.7
### Removed
-
### Fix
- pass lang_obj in context in productslider and signup page oe home page



## [1.0.8] - 2017-10-13
### Added
- Add the marketplace page in app "/mobikul/markeplace"
### Changed
- version from 1.0.7 to 1.0.8
### Removed
-
### Fix
-

## [1.0.9] - 2017-11-15
### Added
- Add the code in payment acquirer api
### Changed
- version from 1.0.8 to 1.0.9
### Removed
-
### Fix
-

## [1.0.10] - 2018-2-14
### Added
- Add api of marketplace
      1)  http://192.168.1.145:8010/mobikul/customer/signUp

        {
        "name":"efgh",
        "login":"efgh@webkul.com",
        "password":1223,
        "is_seller":true,
        "url_handler":"efgh"
        }
        ----------------------------------------------------------------------------------------

      2)  http://192.168.1.145:8010/mobikul/marketplace/seller/orderlines
        POST
        login header with seller
        {
        "state":"new",
        "offset":0,
        "limit":10
        }
        Note: state is not mandatory if state present then response is on the bassis of state
        ----------------------------------------------------------------------------------------
      3)  http://192.168.1.145:8010/mobikul/marketplace/seller/orderline/35
        GET
        login header with seller
        ----------------------------------------------------------------------------------------

      4)  http://192.168.1.145:8010/mobikul/marketplace/seller/ask
        POST
        login header with seller

        {
        "body":"<p><b>hellow boss<b></p><p>howmany products seller add</p>"
        }
        -------------------------------------------------------------------------------------------

      5)  http://192.168.1.145:8010/mobikul/marketplace/seller/product
        POST
        login header with seller

        {
        "state":"approved",
        "operator":"=",
        "offset":0,
        "limit" :10
        }

        Note: operator is on the state filter you can also use operator "!=" or "="

        ------------------------------------------------------------------------------------------------

       6) http://192.168.1.145:8010/mobikul/marketplace/seller/dashboard
        GET
        login header with seller
        -------------------------------------------------------------------------------------------------

  - implement banneer in api "http://192.168.1.145:8010/mobikul/marketplace"



### Changed
- version from 1.0.8 to 1.0.9
### Removed
-
### Fix
-


### Changed Major version
- version from 1.0.10 to 1.1.0
### Removed
-
### Fix
-
### Add
- Add field in mobikul category from category merge ie. website_categ_id
- add field in public.product.category from category merge ie. mobikul_cat_id


### Changed Major version
- version from  1.1.0 to 1.2.0
### Removed
-
### Fix
-
### Add
- Add productId and templateId in wishlist api
- optimize /mobikul/template api
