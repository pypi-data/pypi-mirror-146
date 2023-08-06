from proto_topy.entities import ProtoCollection, ProtoModule, CompilationFailed
import pytest
from pathlib import Path
from distutils.spawn import find_executable
import os

protoc_path = Path(find_executable("protoc") or os.environ.get('PROTOC'))


def test_compile_large_proto():
    module_name = "place"
    proto = ProtoModule(file_path=f"com/here/platform/opensearch/schema/v2/{module_name}.proto", source="""
// This file is part of the OpenSearch API.
// Copyright (c) HERE 2019. All rights reserved.
//
// This software, including documentation, is protected by copyright controlled by HERE.
// All rights are reserved. Copying, including reproducing, storing, adapting or translating,
// any or all of this material requires the prior written consent of HERE.
// This material also contains confidential information which may not be disclosed to
// others without the prior written consent of HERE.

syntax = "proto3";

package com.here.platform.opensearch.schema.v2;

option java_multiple_files = true;
option java_package = "com.here.platform.opensearch.schema.v2";

import "com/here/schema/rib/v2/datetime.proto";

import "com/here/platform/opensearch/schema/v2/common.proto";
import "com/here/platform/opensearch/schema/v2/names.proto";
import "com/here/platform/opensearch/schema/v2/street_names.proto";
import "com/here/platform/opensearch/schema/v2/house_numbers.proto";
import "com/here/platform/opensearch/schema/v2/admin.proto";
import "com/here/platform/opensearch/schema/v2/geometry.proto";
import "com/here/platform/opensearch/schema/v2/storage.proto";

import "google/protobuf/timestamp.proto";

// The Place message represents a POI like a bar, restaurant or shopping mall, a landmark like parks,
// lakes or rivers or any other search result that has an address but also has additional meta information.
//
// For disputes, a Place has an admin hierarchy reference for every unique set of political views.
message Place {

  // Stable RiB/Storage identifier of the Place, in the format of domain:system:type:id,
  // for example, "here:cm:place:3455277". The id part is usually equal to the legacy ppid (and can thus be derived).
  ID id = 1;

  // The place's names and their language variants
  NamesRef names = 2;
  // Names of the street the place is on and their language variants
  StreetNamesRef street_names = 3;

  // This is Admin Hierarchy of the primary contact address of the place. It may not be exactly where the
  // POI is actually located but when sending a letter to the POI this is what would be used as a target address
  //
  // If disputed, multiple hierarchies for every (set of) political view(s)
  repeated AdminHierarchyRef admin_hierarchy = 4;

  // Point address of the place, for navigation and addressing purposes
  PointAddress point_address = 5;

  // Additional access routes that can be used for routing to the POI. E.g. for a park the primary
  // address would be the address of the adminstrators office and we'd have an additional entry
  // for the actual geographic context of the park itself.
  repeated AccessWay additional_access = 6;

  // all categories the place has assigned by their source suppliers including the pds categories and cuisine types
  // all chains that the place belongs to
  // - pds categories are in the format nnn-nnnn-nnn
  // - pds cuisine types are following the format nnn-nnn
  // - chains are integers
  repeated PlaceCategoryRef category = 7;

  // List of suppliers with their ids for the place content
  repeated SupplierIdentifierRef supplier_identifier = 8;

  // Optional importance number for this place
  int64 importance_count = 9;

  // Whether this is an important/prominent place
  bool prominent = 10;

  // TODO Remove field. OpeningInfo replaces this field.
  // Operating times for a place.
  repeated com.here.schema.rib.v2.DateTimeModifier opening_hours = 11 [deprecated=true];

  // Opening times for a category within a place.
  repeated OpeningInfo opening_info = 27;

  // Contact information for a place e.g. homepage, phone number or social media URL
  repeated ContactInfo contact_info = 12;

  // Feedback (reviews, ratings, etc.) by supplier about a place.
  repeated Feedback feedback = 13;

  // TODO: I couldn't find this one in the rib, we need to figure out how to get it, maybe it is deprecated?
  bool permanently_closed = 14;

  // All place ids that have been blended together into this place. Required for clicks etc tracking.
  // Those ids should be alternative ids to access this place on the details page.
  repeated string alternative_id = 15;

  // Payment information for this place.
  repeated PaymentInfo payment = 16;

  // Ranking signals to be merged on OptiMap level, such as search result clicks, number of navigation events
  // and other user interaction we track. This may need to move to somewhere common between address and place
  repeated RankingSignal ranking_signal = 17;

  // all attributes only relevant for public transport hubs like train stations, airports or big harbors
  TransportHubAttributes transport_hub_attributes = 18;

  // attributes related to ev charging stations
  EvChargingAttributes ev_charging_attributes = 19;

  // attributes related to fuel / gas stations
  GasStationAttributes gas_station_attributes = 20;

  // attributes related to trucks
  TruckAttributes truck_attributes = 29;

  // Center point and bounding box of this place
  BasicGeometry geometry = 21;

  // Optional detailed shape of the place
  DetailedGeometry shape = 22;

  // Optional additional storage information (for use in BYOD)
  StorageSupplement storage_supplement = 23;

  // This reflects HERE’s confidence in the accuracy of a Place. It is an integer 1 to 5, where 5 represents highest
  // confidence.
  int32 confidence = 24;

  // Block names for this place
  NamesRef block_names = 25;

  // Sub Block names for this place
  NamesRef sub_block_names = 26;

  // Whether the place is to be deleted for incremental indexing in BYOD
  bool delete = 28;

}

// Reference to a place, a oneof case where either a local reference or the place itself is
// packaged into the message
message PlaceRef {

  oneof oneof_place {
    //The place itself
    Place place = 1;
    //Local reference to the place
    int64 place_ref = 4;
  }
  //Key to the Storage Pool in the map of Storage Pools in the Response
  string storage_pool_key = 3;
}

// Defines a way of accessing a place, which in turn reference additional point addresses
message AccessWay {

  // Type of access
  repeated AccessType access_type = 1;
  // Type of entry
  EntryType entry_type = 2;

  // Optional names of the street the access way is on
  StreetNamesRef street_names = 3;

  // Location and addressing of the access
  PointAddress point_address = 4;

  // Indicates access is restricted (for example, emergency exits, controlled access, private only access).
  bool restricted = 5;

  // Maximum height allowed for access in meters.
  float max_height = 6;
  // Distance to the location in meters
  float distance = 7;

  // block names of the access
  NamesRef block_names = 25;

  // sub block names of the access
  NamesRef sub_block_names = 9;

  // The type of access
  enum AccessType {

    // Used for legacy data where the specific mode/type of access is unknown.
    ACCESS_TYPE_UNKNOWN = 0;

    // Provides access to vehicles for dropping off passengers.
    ACCESS_TYPE_VEHICLE_DROPOFF = 1;

    // Provides access to vehicles for deliveries.
    ACCESS_TYPE_VEHICLE_DELIVERY = 2;

    // Provides vehicle parking for the location.
    ACCESS_TYPE_VEHICLE_PARKING = 3;

    // Provides access to the location via a private drive.
    ACCESS_TYPE_VEHICLE_DRIVEWAY = 4;

    // Provides bicycle parking for the location.
    ACCESS_TYPE_BICYCLE_PARKING = 5;

    // Provides access to the location via a transit stop.
    ACCESS_TYPE_TRANSIT_STOP = 6;

    // Provides access to the building that contains the location.
    ACCESS_TYPE_PEDESTRIAN_PARENT_BUILDING = 7;

    // Provides direct pedestrian access (entrance, exit, walkup) to the location.
    ACCESS_TYPE_PEDESTRIAN_DIRECT = 8;
  }

  // An indication of the directionality of access
  enum EntryType {

    ENTRY_UNKNOWN = 0;
    ENTRY_BOTH = 1;   // Good for both approaching/entering and departing/exiting.
    ENTRY_ENTER = 2;  // Only good for approaching/entering.
    ENTRY_EXIT = 3;   // Only good for departing/exiting.
    ENTRY_NONE = 4;   // Not intended to be entered; for example, a check-in counter or drive-through window.
  }
}

// One source category of a place. If a place has multiple categories from one supplier then
// they are all listed in the category list. If a place has multiple suppliers then each supplier
// has its own list of categories
//
// Categories could be represented as follows with this data construct:
//
// Categories:
//     PlaceCategory:
//         categorySystemId: navteq-lcms
//         category: [300-3000-0000, 550-5510-0202, 350-3550-0336, 550-5510-0204, 400-4100-0042, 300-3000-0023, 800-8600-0186]
//     PlaceCategory:
//         categorySystemId: navteq-poi
//         category: [7999, 7997, 7947, 9707]
//     PlaceCategory:
//         categorySystemId: yelp-categories-alias
//         category: [parks]
//
message PlaceCategory {

  // the id of the category system as taken from RiB CategorySystem.identifier
  oneof oneof_category_system_id {
    // The category system id itself
    string category_system_id = 1;
    // Known category system identifier
    KnownCategorySystem known_category_system_id = 4;
  }

  // true if the category is a primary descriptor of the place.
  bool primary = 5;

  // the category id. Taken from rib Category.identifier
  repeated string category = 2;

  // the names and language variants of a category - index correlated to the 'category' field
  repeated Names category_names = 3;

  // enum of most frequently occurring category system identifiers
  enum KnownCategorySystem {

    CATEGORY_SYSTEM_UNKNOWN = 0;

    CATEGORY_SYSTEM_NOKIA_FOODTYPE = 1;        //nokia-foodtype
    CATEGORY_SYSTEM_NAVTEQ_POI = 2;            //navteq-poi
    CATEGORY_SYSTEM_NAVTEQ_LCMS = 3;           //navteq-lcms
    CATEGORY_SYSTEM_YELP_CATEGORIES_ALIAS = 4; //yelp-categories-alias
    CATEGORY_SYSTEM_NAICS = 5;                 //naics
    CATEGORY_SYSTEM_CHAINS = 6;                //chains
  }
}

// Reference to an Place Category, a oneof case where either a local reference or the Place Category itself is
// packaged into the message
message PlaceCategoryRef {

  oneof oneof_place_category {
    // The place category itself
    PlaceCategory place_category = 1;
    // Local reference to the place category
    int64 place_category_ref = 2;
  }
  // Key to the Storage Pool in the map of Storage Pools in the Response
  string storage_pool_key = 3;
}

// condensed from com/here/schema/rib/v2/ExternalIdentifierAttribute
message SupplierIdentifier {

    // Identifier for the supplier. Taken from the RiB Supplier identifier.
    // will only be non-empty if supplier is not one of the most commonly
    // encountered suppliers.
    oneof oneof_supplier_id {
      // The supplier id iteself
      string supplier_id = 1;
      // Known supplier identifier
      KnownSupplierType known_supplier_id = 3;
    }

    // External place identifier provided by the supplier.
    string external_id = 2;

    // enum of most frequently occurring supplier identifiers
    enum KnownSupplierType {

      SUPPLIER_UNKNOWN = 0;

      HERE_CM_PLACESUPPLIER_NAVTEQCORE = 1;           //here:cm:placesupplier:navteqcore
      HERE_CM_PLACESUPPLIER_LOCALEZE = 2;             //here:cm:placesupplier:localeze
      HERE_CM_PLACESUPPLIER_YELP  = 3;                //here:cm:placesupplier:yelp
      HERE_CM_PLACESUPPLIER_NAVTEQEL = 4;             //here:cm:placesupplier:navteqel
      HERE_CM_PLACESUPPLIER_YELLOWSTONE = 5;          //here:cm:placesupplier:yellowstone
      HERE_CM_PLACESUPPLIER_NAVTEQBASEEL = 6;         //here:cm:placesupplier:navteqbaseel
      HERE_CM_PLACESUPPLIER_TRIPADVISOR = 7;          //here:cm:placesupplier:tripadvisor
      HERE_CM_PLACESUPPLIER_YELLOWSTONE_CREATE = 8;   //here:cm:placesupplier:yellowstone_create
      HERE_CM_PLACESUPPLIER_MAP_COMMUNITY = 9;        //here:cm:placesupplier:map_community
      HERE_CM_PLACESUPPLIER_PUBLIC_TRANSIT = 10;      //here:cm:placesupplier:public_transit
      HERE_CM_PLACESUPPLIER_YEXT = 11;                //here:cm:placesupplier:yext

      HERE_PDS_PLACESUPPLIER_NAVTEQCORE = 12;         //here:pds:placesupplier:navteqcore
      HERE_PDS_PLACESUPPLIER_LOCALEZE = 13;           //here:pds:placesupplier:localeze
      HERE_PDS_PLACESUPPLIER_YELP  = 14;              //here:pds:placesupplier:yelp
      HERE_PDS_PLACESUPPLIER_NAVTEQEL = 15;           //here:pds:placesupplier:navteqel
      HERE_PDS_PLACESUPPLIER_YELLOWSTONE = 16;        //here:pds:placesupplier:yellowstone
      HERE_PDS_PLACESUPPLIER_NAVTEQBASEEL = 17;       //here:pds:placesupplier:navteqbaseel
      HERE_PDS_PLACESUPPLIER_TRIPADVISOR = 18;        //here:pds:placesupplier:tripadvisor
      HERE_PDS_PLACESUPPLIER_YELLOWSTONE_CREATE = 19; //here:pds:placesupplier:yellowstone_create
      HERE_PDS_PLACESUPPLIER_MAP_COMMUNITY = 20;      //here:pds:placesupplier:map_community
      HERE_PDS_PLACESUPPLIER_PUBLIC_TRANSIT = 21;     //here:pds:placesupplier:public_transit
      HERE_PDS_PLACESUPPLIER_YEXT = 22;               //here:pds:placesupplier:yext

      HERE_SOCIAL_SIGNAL_SUPPLIER_YELLOWSTONE_SIGNALS = 23; // RiB SocialSignal.attribute_type: YELLOWSTONE-SIGNALS
      HERE_OS_CLICK_ACTIVITY = 24; // OpenSearch Click Activity. See catalog layer hrn:here:data:::here-opensearch-external-content-for-optimized-map-3:places-click-activity
    }
}

// Reference to an Supplier Identifier, a oneof case where either a local reference or the Supplier Identifier itself is
// packaged into the message
message SupplierIdentifierRef {

  oneof oneof_supplier_identifier {
    //The supplier identifier itself
    SupplierIdentifier supplier_identifier = 1;
    //Local reference to the supplier identifier
    int64 supplier_identifier_ref = 2;
  }
  //Key to the Storage Pool in the map of Storage Pools in the Response
  string storage_pool_key = 3;
}

// Contact information for a place.
// Re-defined here to avoid dependency on RiB.
message ContactInfo {

  // Determines the type of contact information in the value.
  ContactType type = 1;

  // Contact information, as specified by the contact type.
  string value = 2;

  // Label for the contact string, such as "Customer Service" or "Pharmacy Fax".  Optional.
  Text label = 3;

  // Department/category within a large place to which the contact information applies.
  // For example, a pharmacy of Walmart may have category "here:pds:navteq-lcms:700-7400-0292"
  repeated PlaceCategoryRef category_ref = 4;

  // Contact type values.
  enum ContactType {

    CONTACT_TYPE_UNKNOWN = 0;
    CONTACT_TYPE_NAME = 1;          // A person's name
    CONTACT_TYPE_EMAIL = 2;         // Email address
    CONTACT_TYPE_PHONE = 3;         // Phone number
    CONTACT_TYPE_FAX = 4;           // Fax number
    CONTACT_TYPE_SOCIAL = 5;        // Skype, Facebook, Twitter, etc.
    CONTACT_TYPE_IM = 6;            // Instant Messaging ID
    CONTACT_TYPE_MOBILE_PHONE = 7;  // Mobile phone number
    CONTACT_TYPE_TOLL_FREE = 8;     // Toll-free telephone number
    CONTACT_TYPE_WEB_ADDRESS = 9;   // Website address
    CONTACT_TYPE_OTHER = 10;        // Type alignment with RiB, no further description provided
  }
}

message OpeningInfo {

  // Indicates that the Place is open 24 hours per day, 7 days per week when set to true.
  bool always_open = 1;

  repeated com.here.schema.rib.v2.DateTimeModifier opening_hours = 2;

  // Department/category within a large place to which the contact information applies.
  // For example, a pharmacy of Walmart may have category "here:pds:navteq-lcms:700-7400-0292"
  repeated PlaceCategoryRef category_ref = 3;
}

// Information about payment types that are either known to be accepted or not.
// Re-defined here to avoid dependency on RiB.
message PaymentInfo {

  // Payment type.
  PaymentType payment_type = 2;

  // Qualifiers for the payment type.
  // For CASH, it may contain the currency type.
  // For CREDITCARD, it may contain the card types that are accepted.
  repeated string type_qualifier = 3;

  // Whether the payment type is accepted or not.
  bool accepted = 4;

  // Department/category within a large place to which the contact information applies.
  // For example, a pharmacy of Walmart may have category "here:pds:navteq-lcms:700-7400-0292"
  repeated PlaceCategoryRef category_ref = 5;

  // Type of payment
  enum PaymentType {

    PAYMENT_TYPE_UNDEFINED = 0;
    PAYMENT_TYPE_OTHER = 1;
    PAYMENT_TYPE_DEBITCARD = 2;
    PAYMENT_TYPE_CASH = 3;
    PAYMENT_TYPE_CREDITCARD = 4;
    PAYMENT_TYPE_CHEQUE = 5;
    PAYMENT_TYPE_EPAYMENT = 6;
    PAYMENT_TYPE_MONEY_CARD = 7;
    PAYMENT_TYPE_NFC = 8;
    PAYMENT_TYPE_PHONE = 9;
    PAYMENT_TYPE_SMS = 10;
    PAYMENT_TYPE_PREPAID = 11;
    PAYMENT_TYPE_FUELCARD = 12;
    PAYMENT_TYPE_ADDITIONAL = 13;
  }
}

// attributes only relevant for public transport hubs like train stations, airports or big harbors go into this message
message TransportHubAttributes {
    int64 passenger_count = 1;
}

// attributes only relevant to ev charging stations such as plug types, network offering the station, voltage and amperage
message EvChargingAttributes {

   // total number of charging points/places at the station := sum of ports over all available connector types
   uint32 total_number_of_connectors = 4;

   // unique list of connector types; rendered as connector list
   repeated PortCharacteristics port = 1;

   EVProvider provider               = 3;

   Access access = 2;

   enum Access {
     ACCESS_UNDEFINED = 0;
     UNRESTRICTED = 1;
     GENERIC_RESTRICTION = 2;
     RESIDENTS = 3;
     EMPLOYEES = 4;
     AUTHORIZED_PERSONNEL = 5;
     MEMBERS = 6;
     RESERVABLE = 7;
   }

   // a voltage or amperage range (inclusive for both lower and upper bound)
   message NumberRange {
       int32 from = 1;
       int32 to = 2;
   }

  // The attributes of the charging port. Such as amperage, voltage and the plug type. Also how many
  // slots are available for a port with this type.
  message PortCharacteristics {

    // either electric or hydrogen
    EvType type                     = 1;

    // EMobilityPlugType is --Deprecated-- and is replaced by ConnectorType
    EMobilityPlugType em_plug_type  = 2 [deprecated = true];

    H2PlugType h2_plug_type         = 3;

    // rendered as supplier name: example: "ChargePoint"
    EVProvider supplier             = 13;

    // A connector is the (male and female) plug type that connects a vehicle to the charging point.
    ConnectorType connector_type    = 17;

    // power feed type
    PowerFeedType power_feed_type   = 14;

    // AC or DC. applies to EMobility only
    Current current                 = 6;

    // applies for H2 (hydrogen) only (units?)
    int32 pressure                  = 7;

    bool fixed_cable                = 8;

    // the power level in kilowatts rendered as -> {max_power_level}, example: "6.60"
    float power_level_kilowatts     = 10;

    // if the port is restricted to private access only
    bool private_access             = 11;

    // the charging level of the port as defined at https://en.wikipedia.org/wiki/Electric_car#US_charging_standards
    int32 customer_charge_level     = 12;

    // ChargingPoint attributes
    // -----------------------
    // stored as an enum, should be rendered as a string
    ChargeMode charge_mode          = 16;

    // number of physical connectors at the charge point, rendered as number_of_connectors
    int32 number_of_slots           = 9;

    // phase
    uint32 phase                    = 15;

    // amperage in unit Ampere, rendered as amps range: examples 16A, 12A-80A or 200A.
    NumberRange amperage            = 4;

    // voltage in unit Volt, rendered as volts range: examples 100-120V AC or 600V DC.
    NumberRange voltage             = 5;

    enum ChargeMode {
        CHARGE_MODE_UNKNOWN = 0; // Unspecified – no information provided
        MODE_1              = 1; // slow charging from a regular electrical socket (1 or 3 phase)
        MODE_2              = 2; // slow charging from a regular socket equipped with some EV specific protection
        // arrangement. Examples include Park & Charge and PARVE systems.
        MODE_3              = 3; // slow or fast charging using a specific EV multi-pin socket with control and
        // protection functions. Examples include systems with SAE J1772 and IEC 62196 connectors.
        MODE_4              = 4; // fast charging using some special charging technology such as CHAdeMO.
    }

    // the current of the port (AC or DC)
    enum Current {
      CURRENT_UNDEFINED = 0;
      AC = 1;
      DC = 2;
    }

    // either electric or hydrogen
    enum EvType {
      EVTYPE_UNDEFINED = 0;
      EMOBILITY = 1;
      H2 = 2;
    }

    // Source http://charon.cutlass.nokia.com:8000/clio_cli_output/1592837052/topics-auto/resource-types-ev.html#list-of-powerfeedtype-values
    enum PowerFeedType {
        POWER_FEED_UNKNOWN = 0; // Unspecified
        LEVEL_1            = 1; // In the Americas, this level covers connectors operating at 120VAC @ 16A. In Australia,
        // this level covers connectors operating at 240VAC @ 15A.
        LEVEL_2            = 2; // In the Americas, this level covers connectors operating at 208/240VAC @ 30A. In
        // Australia, this level covers connectors operating at 240VAC @ 16A.
        LEVEL_3            = 3; // In Australia, this level covers connectors operating at 240VAC @ 32A.
        LEVEL_5            = 6;
        POWER_FEED_OTHER   = 4; // Value not specified
        DC_FAST_CHARGE     = 5; // In the Americas, this level covers connectors operating at 600VDC max @ 200A max.
    }


    // --Deprecated-- the type of the electric plug. Replaced by ConnectorType below.
    enum EMobilityPlugType {
        EM_PLUG_TYPE_UNDEFINED = 0;
        OTHER = 1;
        TYP2 = 2;
        IEC60309_3P_E_N = 3;
        IEC60309_P_E_N = 4;
        SCHUKO = 5;
        YAZAKI = 6;
        CHA_DE_MO = 7;
        J1772 = 8;
        J1772_COMBO = 9;
        BS_1363 = 10;
        MK_COMMANDO_K9785 = 11;
        TESLA_CONNECTOR = 12;
        NEMA_5 = 13;
        NEMA_14_30 = 14;
        NEMA_14_50 = 15;
        NEMA_6_20 = 16;
        COMBINED_CS = 17;
        TYP3 = 18;
        DANISH_SECTION_2_D1 = 19;
        MARECHAL_DEKONTAKTOR = 20;
        TESLA_SUPERCHARGER = 21;
        JEVS_G_105 = 22;
        AC_DC_COMBO_MENNEKES_TYPE_2 = 23;
        DC_TEPCO = 24;
    }

    // the type of hydrogen refueling
    enum H2PlugType {
      H2_PLUG_TYPE_UNDEFINED = 0;
      BUS_CGH2 = 1;
      CGH2 = 2;
      CAR_CGH2 = 3;
      LH2 = 4;
    }
  }

   // A connector is the (male and female) plug type that connects a vehicle to the charging point.
   // name_type and number_id are only filled if connector type is not a known type.
   message ConnectorType {

       oneof oneof_connector_name {

           // known connector types are represented by enumerations
           KnownConnectorType known_type = 2;

           // name string of a connector type not matching any in KnownConnectorType
           string name = 3;
       }

       // A connector is the (male and female) plug type that connects a vehicle to the charging point.
       // Not all EV Stations provide the necessary cabling to connect a vehicle to the charging point.
       // Source http://charon.cutlass.nokia.com:8000/clio_cli_output/1592837052/topics-auto/resource-types-ev.html#list-of-connectortype-values
       enum KnownConnectorType {
           CONNECTOR_TYPE_UNKNOWN                          = 0;  // 	Unspecified
           CONNECTOR_TYPE_OTHER                            = 1;  // 	Other
           CONNECTOR_TYPE_UNALLOWED                        = 2;  // 	Unallowed
           SMALL_PADDLE_INDUCTIVE                          = 3;  // 	Small Paddle Inductive
           LARGE_PADDLE_INDUCTIVE                          = 4;  // 	Large Paddle Inductive
           DOMESTIC_SOCKET_TYPE_B_NEMA_5_15                = 5;  // 	Domestic plug/socket type B (NEMA 5-15)
           DOMESTIC_SOCKET_TYPE_B_NEMA_5_20                = 6;  // 	Domestic plug/socket type B (NEMA 5-20)
           DOMESTIC_SOCKET_TYPE_D_BS_546_3_PIN             = 7;  // 	Domestic plug/socket type D (BS 546 (3 pin))
           DOMESTIC_SOCKET_TYPE_E_CEE_7_5                  = 8;  // 	Domestic plug/socket type E (CEE 7/5)
           DOMESTIC_SOCKET_TYPE_F_CEE_7_4_SCHUKO           = 9;  // 	Domestic plug/socket type F (CEE 7/4 (Schuko))
           DOMESTIC_SOCKET_TYPE_E_F_CEE_7_7                = 10; // 	Domestic plug/socket type E+F (CEE 7/7)
           DOMESTIC_SOCKET_TYPE_G                          = 11; // 	Domestic plug/socket type G (BS 1363, IS 401 & 411, MS 58)
           DOMESTIC_SOCKET_TYPE_H_SI_32                    = 12; // 	Domestic plug/socket type H (SI 32)
           DOMESTIC_SOCKET_TYPE_I_AS_NZS_3112              = 13; // 	Domestic plug/socket type I (AS/NZS 3112)
           DOMESTIC_SOCKET_TYPE_I_CPCS_CCC                 = 14; // 	Domestic plug/socket type I (CPCS-CCC)
           DOMESTIC_SOCKET_TYPE_I_IRAM_2073                = 15; // 	Domestic plug/socket type I (IRAM 2073)
           DOMESTIC_SOCKET_TYPE_J_SEV_1011_T13             = 16; // 	Domestic plug/socket type J (SEV 1011) (T13)
           DOMESTIC_SOCKET_TYPE_J_SEV_1011_T15             = 17; // 	Domestic plug/socket type J (SEV 1011) (T15)
           DOMESTIC_SOCKET_TYPE_J_SEV_1011_T23             = 18; // 	Domestic plug/socket type J (SEV 1011) (T23)
           DOMESTIC_SOCKET_TYPE_J_SEV_1011_T25             = 19; // 	Domestic plug/socket type J (SEV 1011) (T25)
           DOMESTIC_SOCKET_TYPE_K_SECTION_107_2_D1         = 20; // 	Domestic plug/socket type K (Section 107-2-D1)
           DOMESTIC_SOCKET_TYPE_K_THAILAND_TIS             = 21; // 	Domestic plug/socket type K (Thailand TIS 166 - 2549)
           DOMESTIC_SOCKET_TYPE_L_CEI_23_16                = 22; // 	Domestic plug/socket type L (CEI 23-16/VII)
           DOMESTIC_SOCKET_TYPE_M_SOUTH_AFRICAN_15_A_250_V = 23; // 	Domestic plug/socket type M (South African 15 A/250 V)
           DOMESTIC_SOCKET_TYPE_IEC_60906_1_3_PIN          = 24; // 	Domestic plug/socket type IEC 60906-1 (3 pin)
           AVCON_CONNECTOR                                 = 25; // 	AVCON Connector
           TESLA_CONNECTOR_HIGH_POWER_WALL                 = 26; // 	Tesla Connector (high power wall)
           TESLA_CONNECTOR_UNIVERSAL_MOBILE                = 27; // 	Tesla Connector (universal mobile)
           TESLA_CONNECTOR_SPARE_MOBILE                    = 28; // 	Tesla Connector (spare mobile)
           JEVS_G_105_CHADEMO                              = 29; // 	JEVS G 105 (CHAdeMO)
           IEC_62196_2_TYPE_1_SAE_J1772                    = 30; // 	IEC 62196-2 type 1 (SAE J1772)
           IEC_62196_2_TYPE_2_MENNEKES                     = 31; // 	IEC 62196-2 type 2 (Mennekes)
           IEC_62196_2_TYPE_3C_SCAME                       = 32; // 	IEC 62196-2 type 3c (SCAME)
           IEC_62196_3_TYPE_1_COMBO_SAE_J1772              = 33; // 	IEC 62196-3 type 1 combo (SAE J1772)
           IEC_62196_3_TYPE_2_COMBO_MENNEKES               = 34; // 	IEC 62196-3 type 2 combo (Mennekes)
           IEC_60309_INDUSTRIAL_P_N_E_AC                   = 35; // 	IEC 60309 : industrial P + N + E (AC)
           IEC_60309_INDUSTRIAL_3P_E_N_AC                  = 36; // 	IEC 60309 : industrial 3P + E + N (AC)
           IEC_60309_INDUSTRIAL_2P_E_AC                    = 37; // 	IEC 60309 : industrial 2P + E (AC)
           IEC_60309_INDUSTRIAL_P_N_E_AC_CEEPLUS           = 38; // 	IEC 60309 : industrial P + N + E (AC) (CEEPlus)
           IEC_60309_INDUSTRIAL_3P_N_E_AC_CEEPLUS          = 39; // 	IEC 60309 : industrial 3P + N + E (AC) (CEEPlus)
           BETTER_PLACE_SOCKET                             = 40; // 	Better place plug/socket
           MARECHAL_SOCKET                                 = 41; // 	Marechal plug/socket
           DOMESTIC_SOCKET_TYPE_J_SEV_1011_T13_T23         = 42; // 	Domestic plug/socket type J (SEV 1011) (T13, T23)
           TESLA                                           = 43; // 	Tesla Connector
           IEC_61851_1                                     = 44; // 	IEC 61851-1
           IEC_62196_2_TYPE_2_SAE_J1772                    = 45; // 	IEC 62196-2 type 2 (SAE J1772)
           I_E_C_60309_INDUSTRIAL_2P_PLUS_E_DC             = 46; // 	IEC 60309 : industrial 2P + E (DC)
           I_TYPE_AS_NZ_3112_AUSTRALIAN_15_A_240_V         = 47; // 	I-type AS/NZ 3112 (Australian 15A/240V)
           DOMESTIC_SOCKET_TYPE_A_NEMA_1_15                = 48; //    Domestic plug/socket type A (NEMA 1-15, 2 pins)
           DOMESTIC_SOCKET_TYPE_C_CEE_7_17_2_PIN           = 49; //    Domestic plug/socket type C (CEE 7/17, 2 pins)
           IEC_62196_2_TYPE_3A_SCAME                       = 50; //    IEC 62196-2 type 3a (SCAME)
           DOMESTIC_SOCKET_TYPE_B_NEMA_14_50               = 51; //    Domestic plug/socket type B (NEMA 14-50)
           GB_T_CHINESE_AC_CONNECTOR                       = 52; //    GB/T (Chinese) AC connector
           GB_T_CHINESE_DC_CONNECTOR                       = 53; //    GB/T (Chinese) DC connector
       }
   }

  // the provide of the ev charging service
  message EVProvider {

    ProviderKind kind = 1;
    ProviderCode code = 2;

    string provider = 3;

    enum ProviderKind {
      KIND_UNDEFINED = 0;
      PRIVATE = 1;
      COMMERCIAL = 2;
    }

    enum ProviderCode {
      CODE_UNDEFINED = 0;
      ADAC = 1;
      AERO_VIRONMENT_NETWORK = 2;
      BELECTRIC_DRIVE = 3;
      BLINK_NETWORK = 4;
      CEZ = 5;
      CHARGE_POINT_NETWORK = 6;
      E_LAAD = 7;
      ENBW = 8;
      EON = 9;
      EVGO_NETWORK = 10;
      GREENLOTS = 11;
      KOETTGEN = 12;
      LADEFOXX = 13;
      LADENETZ = 14;
      MAINOVA = 15;
      OP_CONNECT = 16;
      OPEN_CHARGE_MAP = 17;
      RECHARGE_ACCESS = 18;
      SEMA_CHARGE_NETWORK = 19;
      SHOREPOWER = 20;
      RWE = 21;
      STADTWERKE_BOCHUM = 22;
      STADTWERKE_KARLSRUHE = 23;
      STADTWERKE_LEIPZIG = 24;
      STADTWERKE_MUENCHEN = 25;
      VATTENFALL = 26;
    }
  }
}

// place attributes and amenities related to trucks.
message TruckAttributes {

    // amenities related to trucks
    enum TruckAttributeType {
        TRUCK_ATTRIBUTE_TYPE_UNKNOWN = 0;  // unknown truck attribute type
        WIFI                         = 1;  // Whether or not the truck stop offers wifi
        IDLE_REDUCTION               = 2;  // Idle reduction describes technologies and practices that minimize
                                           // the amount of time drivers idle their engines.
        SERVICE                      = 3;  // Can truck be truck be repaired and serviced.
        WEIGH_STATION                = 4;  // Indicates if truck scales are available onsite or nearby.
        ONSITE_SHOWER                = 5;  // The place has showers onsite.
        WASH                         = 6;  // Trucks can be washed onsite.
        PARKING                      = 7;  // truck parking is available.
        SECURE_PARKING               = 8;  // Secure parking is available.
        ONLY_NIGHT_PARKING           = 9;  // Trucks may only park at night.
        HIGH_CANOPY                  = 10; // Fuel station accommodates trucks with a high canopy.
        TRUCK_STOP                   = 11; // Does the place have or is the place a truck stop.
    }

    // list of truck amenities attributable to the place
    repeated TruckAttributeType available_attributes = 1;

    // list of truck amenities that the place does not have
    repeated TruckAttributeType unavailable_attributes = 2;

    // The number of showers onsite.
    uint32 number_of_showers = 3;
}

// Attributes related to gas stations go here such as fuel types sold, what other services are available
message GasStationAttributes {

    enum FuelType {
        FUEL_TYPE_UNKNOWN     = 0;   // unknown type
        DIESEL                = 1;   // diesel
        DIESEL_WITH_ADDITIVES = 2;   // diesel with additives
        BIODIESEL             = 3;   // biodiesel
        GASOLINE              = 4;   // gasoline/benzin/petrol
        ETHANOL               = 5;   // ethanol
        CNG                   = 6;   // compressed natural gas
        LPG                   = 7;   // liquified petroleum gas
    }

    // available fuels
    repeated FuelType available_fuels = 1;

    // not available fuels
    repeated FuelType unavailable_fuels = 2;

    // can customers pay at pump
    bool pay_at_pump = 3;

    // are there high volume pumps
    bool high_volume_pumps = 4;
}

// A ranking signal based on clicks and other signals that indicate the
// prominence of a place. For now all signals are global for the associated
// place but later we may restrict the scope of a signal to a region or country.
message RankingSignal {
  SignalType signal_type = 1;

  float value = 2;

  SupplierIdentifierRef supplier_ref = 3;

  enum SignalType {
    SIGNAL_TYPE_UNKNOWN = 0; // should actually never happen
    DETAILS_FETCHED = 1; // How often the place details have been fetched
    ROUTING_REQUESTED = 2; // how often a route was calculated to this place
    NAVIGATION_REQUESTED = 3; // how often a user actually started step-by-step navigation to this place
    PHONE_CALL_REQUESTED = 4; // how often the place was called
    TOTAL_CLICKS = 5; // total # of clicks for a place
    CHECKINS = 6; // number of checkins in social media
    LIKES = 7; // number of likes in social media
    // more to come
  }
}

// All Feedback (reviews, ratings, etc.) of a certain supplier about a place.
// Inspired by the RiB Feedback message. Re-defined here to avoid dependency on RiB.
message Feedback {

  // The id of the supplier
  string supplier_id = 2;

  // Descriptions in the feedback.
  repeated Text description = 3;

  // Media linked to the feedback.
  repeated LinkedMedia linked_media = 4;

  // Reviews in the feedback.
  repeated Review review = 5;

  // Aggregated rating and count in the feedback.
  repeated AggregatedRating rating = 6;

  // Linked media file.
  message LinkedMedia {

    // Title of media.
    Text title = 1;

    // URL of media.
    string url = 2;

    // Type of media.  For example, image, audio, or video.
    MediaType type = 3;

    // Created timestamp.
    google.protobuf.Timestamp created = 4;

    // Leaving out the author for now. We may need it for exposing rich data, we can still add it then
    // repeated Name author_name = 5;
  }

  // Type of media.
  enum MediaType {

    MEDIA_TYPE_UNKNOWN = 0;
    MEDIA_TYPE_AUDIO = 1;
    MEDIA_TYPE_VIDEO = 2;
    MEDIA_TYPE_IMAGE = 3;
  }

  // Review of a place.
  message Review {

    // Title of the review.
    Text title = 1;

    // Rating that was provided as part of this review.
    // In RiB the model provides several ratings for one review, but it's most likely a bug, since they forgot to include
    // what category the rating belongs to. So we'll just store the average rating here
    Rating rating = 2;

    // Review text.
    Text review = 3;
  }

  // Rating of a place.
  message Rating {

    // The rating's value (for example, 4 out of 5 star rating has a value of 4).
    float rating = 1;
    // The rating's scale (for example, 4 out of 5 star rating has a scale of 5).
    uint32 scale = 2;
    // Created timestamp.
    google.protobuf.Timestamp created = 3;
  }

  // Aggregated rating information about a place
  message AggregatedRating {

    // Average rating.
    float average_rating = 1;
    // Number of ratings that contributed to the average.
    uint64 rating_count = 2;
    // Number of ratings that contributed to the average that were from full reviews.
    uint64 review_count = 3;
  }
}
    """)
    proto_dict = ProtoCollection(protoc_path, proto)
    proto_dict.compile()

