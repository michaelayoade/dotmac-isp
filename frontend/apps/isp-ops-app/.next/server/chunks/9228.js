"use strict";exports.id=9228,exports.ids=[9228],exports.modules={19228:(e,t,i)=>{i.d(t,{$jX:()=>ea,Bvd:()=>eT,GqX:()=>_,Grg:()=>c,Gv9:()=>eq,HJO:()=>eh,JnJ:()=>eg,LV7:()=>eP,SlU:()=>eo,UG2:()=>X,VHq:()=>eR,XAI:()=>n,XIX:()=>ei,_A2:()=>ee,a3z:()=>V,aQl:()=>y,cji:()=>el,d5j:()=>A,gBt:()=>Y,iTI:()=>eS,j_N:()=>em,k9y:()=>er,kwm:()=>I,lck:()=>eI,nnH:()=>k,o2N:()=>ez,sNp:()=>H,sh8:()=>eD,tFq:()=>eL,tet:()=>eC,udL:()=>z,v6w:()=>j,wmV:()=>$,xFP:()=>ek,yGZ:()=>eM,zbi:()=>s,zvb:()=>P});var s,a,n,r,c,o,d,l,u,m,p,I,y,g,A,P,v,S,b,C,$,h,f,D,N,T,E,R,B,M,U,L=i(77661),O=i(14764);let q={};(function(e){e.Degraded="DEGRADED",e.Maintenance="MAINTENANCE",e.Offline="OFFLINE",e.Online="ONLINE",e.Provisioning="PROVISIONING",e.Rebooting="REBOOTING"})(s||(s={})),function(e){e.ContactMade="CONTACT_MADE",e.Created="CREATED",e.Export="EXPORT",e.Import="IMPORT",e.Login="LOGIN",e.NoteAdded="NOTE_ADDED",e.Purchase="PURCHASE",e.StatusChanged="STATUS_CHANGED",e.SupportTicket="SUPPORT_TICKET",e.TagAdded="TAG_ADDED",e.TagRemoved="TAG_REMOVED",e.Updated="UPDATED"}(a||(a={})),function(e){e.Critical="CRITICAL",e.Info="INFO",e.Warning="WARNING"}(n||(n={})),function(e){e.Annual="ANNUAL",e.Custom="CUSTOM",e.Monthly="MONTHLY",e.Quarterly="QUARTERLY",e.Yearly="YEARLY"}(r||(r={})),function(e){e.Aerial="AERIAL",e.Building="BUILDING",e.Buried="BURIED",e.Duct="DUCT",e.Submarine="SUBMARINE",e.Underground="UNDERGROUND"}(c||(c={})),function(e){e.Wifi_2_4="WIFI_2_4",e.Wifi_5="WIFI_5",e.Wifi_6="WIFI_6",e.Wifi_6E="WIFI_6E"}(o||(o={})),function(e){e.Active="ACTIVE",e.Archived="ARCHIVED",e.Churned="CHURNED",e.Inactive="INACTIVE",e.Prospect="PROSPECT",e.Suspended="SUSPENDED"}(d||(d={})),function(e){e.Basic="BASIC",e.Enterprise="ENTERPRISE",e.Free="FREE",e.Premium="PREMIUM",e.Standard="STANDARD"}(l||(l={})),function(e){e.Business="BUSINESS",e.Enterprise="ENTERPRISE",e.Individual="INDIVIDUAL",e.Partner="PARTNER",e.Vendor="VENDOR"}(u||(u={})),function(e){e.Degraded="DEGRADED",e.Offline="OFFLINE",e.Online="ONLINE",e.Unknown="UNKNOWN"}(m||(m={})),function(e){e.Cpe="CPE",e.Firewall="FIREWALL",e.Olt="OLT",e.Onu="ONU",e.Other="OTHER",e.Router="ROUTER",e.Switch="SWITCH"}(p||(p={})),function(e){e.BuildingEntry="BUILDING_ENTRY",e.Cabinet="CABINET",e.Closure="CLOSURE",e.Handhole="HANDHOLE",e.Manhole="MANHOLE",e.Pedestal="PEDESTAL",e.Pole="POLE"}(I||(I={})),function(e){e.Active="ACTIVE",e.Damaged="DAMAGED",e.Decommissioned="DECOMMISSIONED",e.Inactive="INACTIVE",e.Maintenance="MAINTENANCE",e.UnderConstruction="UNDER_CONSTRUCTION"}(y||(y={})),function(e){e.Critical="CRITICAL",e.Excellent="EXCELLENT",e.Fair="FAIR",e.Good="GOOD",e.Poor="POOR"}(g||(g={})),function(e){e.Hybrid="HYBRID",e.MultiMode="MULTI_MODE",e.SingleMode="SINGLE_MODE"}(A||(A={})),function(e){e.Band_2_4Ghz="BAND_2_4_GHZ",e.Band_5Ghz="BAND_5_GHZ",e.Band_6Ghz="BAND_6_GHZ"}(P||(P={})),function(e){e.Ach="ACH",e.BankAccount="BANK_ACCOUNT",e.Card="CARD",e.Cash="CASH",e.Check="CHECK",e.Crypto="CRYPTO",e.DigitalWallet="DIGITAL_WALLET",e.Other="OTHER",e.WireTransfer="WIRE_TRANSFER"}(v||(v={})),function(e){e.Cancelled="CANCELLED",e.Failed="FAILED",e.Pending="PENDING",e.Processing="PROCESSING",e.Refunded="REFUNDED",e.RequiresAction="REQUIRES_ACTION",e.RequiresCapture="REQUIRES_CAPTURE",e.RequiresConfirmation="REQUIRES_CONFIRMATION",e.Succeeded="SUCCEEDED"}(S||(S={})),function(e){e.Admin="ADMIN",e.Analytics="ANALYTICS",e.Automation="AUTOMATION",e.Billing="BILLING",e.Communication="COMMUNICATION",e.Cpe="CPE",e.Customer="CUSTOMER",e.Ipam="IPAM",e.Network="NETWORK",e.Security="SECURITY",e.Ticket="TICKET",e.User="USER",e.Workflow="WORKFLOW"}(b||(b={})),function(e){e.Hybrid="HYBRID",e.OneTime="ONE_TIME",e.Subscription="SUBSCRIPTION",e.UsageBased="USAGE_BASED"}(C||(C={})),function(e){e.Commercial="COMMERCIAL",e.Industrial="INDUSTRIAL",e.Mixed="MIXED",e.Residential="RESIDENTIAL"}($||($={})),function(e){e.Active="ACTIVE",e.Degraded="DEGRADED",e.Failed="FAILED",e.Inactive="INACTIVE"}(h||(h={})),function(e){e.Fusion="FUSION",e.Mechanical="MECHANICAL"}(f||(f={})),function(e){e.Active="ACTIVE",e.Canceled="CANCELED",e.Ended="ENDED",e.Incomplete="INCOMPLETE",e.PastDue="PAST_DUE",e.Paused="PAUSED",e.Trialing="TRIALING"}(D||(D={})),function(e){e.Custom="CUSTOM",e.Enterprise="ENTERPRISE",e.Free="FREE",e.Professional="PROFESSIONAL",e.Starter="STARTER"}(N||(N={})),function(e){e.Active="ACTIVE",e.Cancelled="CANCELLED",e.Inactive="INACTIVE",e.Pending="PENDING",e.Suspended="SUSPENDED",e.Trial="TRIAL"}(T||(T={})),function(e){e.Active="ACTIVE",e.Invited="INVITED",e.Suspended="SUSPENDED"}(E||(E={})),function(e){e.Open="OPEN",e.Wep="WEP",e.Wpa="WPA",e.Wpa2="WPA2",e.Wpa2Wpa3="WPA2_WPA3",e.Wpa3="WPA3"}(R||(R={})),function(e){e.Compensated="COMPENSATED",e.Completed="COMPLETED",e.Failed="FAILED",e.Pending="PENDING",e.RolledBack="ROLLED_BACK",e.RollingBack="ROLLING_BACK",e.Running="RUNNING"}(B||(B={})),function(e){e.Compensated="COMPENSATED",e.Compensating="COMPENSATING",e.CompensationFailed="COMPENSATION_FAILED",e.Completed="COMPLETED",e.Failed="FAILED",e.Pending="PENDING",e.Running="RUNNING",e.Skipped="SKIPPED"}(M||(M={})),function(e){e.ActivateService="ACTIVATE_SERVICE",e.ChangeServicePlan="CHANGE_SERVICE_PLAN",e.DeprovisionSubscriber="DEPROVISION_SUBSCRIBER",e.MigrateSubscriber="MIGRATE_SUBSCRIBER",e.ProvisionSubscriber="PROVISION_SUBSCRIBER",e.SuspendService="SUSPEND_SERVICE",e.TerminateService="TERMINATE_SERVICE",e.UpdateNetworkConfig="UPDATE_NETWORK_CONFIG"}(U||(U={})),(0,L.Ps)`
  query CustomerList(
    $limit: Int = 50
    $offset: Int = 0
    $status: CustomerStatusEnum
    $search: String
    $includeActivities: Boolean = false
    $includeNotes: Boolean = false
  ) {
    customers(
      limit: $limit
      offset: $offset
      status: $status
      search: $search
      includeActivities: $includeActivities
      includeNotes: $includeNotes
    ) {
      customers {
        id
        customerNumber
        firstName
        lastName
        middleName
        displayName
        companyName
        status
        customerType
        tier
        email
        emailVerified
        phone
        phoneVerified
        mobile
        addressLine1
        addressLine2
        city
        stateProvince
        postalCode
        country
        taxId
        industry
        employeeCount
        lifetimeValue
        totalPurchases
        averageOrderValue
        lastPurchaseDate
        createdAt
        updatedAt
        acquisitionDate
        lastContactDate
        activities @include(if: $includeActivities) {
          id
          customerId
          activityType
          title
          description
          performedBy
          createdAt
        }
        notes @include(if: $includeNotes) {
          id
          customerId
          subject
          content
          isInternal
          createdById
          createdAt
          updatedAt
        }
      }
      totalCount
      hasNextPage
    }
  }
`,(0,L.Ps)`
  query CustomerDetail($id: ID!) {
    customer(id: $id, includeActivities: true, includeNotes: true) {
      id
      customerNumber
      firstName
      lastName
      middleName
      displayName
      companyName
      status
      customerType
      tier
      email
      emailVerified
      phone
      phoneVerified
      mobile
      addressLine1
      addressLine2
      city
      stateProvince
      postalCode
      country
      taxId
      industry
      employeeCount
      lifetimeValue
      totalPurchases
      averageOrderValue
      lastPurchaseDate
      createdAt
      updatedAt
      acquisitionDate
      lastContactDate
      activities {
        id
        customerId
        activityType
        title
        description
        performedBy
        createdAt
      }
      notes {
        id
        customerId
        subject
        content
        isInternal
        createdById
        createdAt
        updatedAt
      }
    }
  }
`,(0,L.Ps)`
  query CustomerMetrics {
    customerMetrics {
      totalCustomers
      activeCustomers
      newCustomers
      churnedCustomers
      totalCustomerValue
      averageCustomerValue
    }
  }
`,(0,L.Ps)`
  query CustomerActivities($id: ID!) {
    customer(id: $id, includeActivities: true, includeNotes: false) {
      id
      activities {
        id
        customerId
        activityType
        title
        description
        performedBy
        createdAt
      }
    }
  }
`,(0,L.Ps)`
  query CustomerNotes($id: ID!) {
    customer(id: $id, includeActivities: false, includeNotes: true) {
      id
      notes {
        id
        customerId
        subject
        content
        isInternal
        createdById
        createdAt
        updatedAt
      }
    }
  }
`,(0,L.Ps)`
  query CustomerDashboard(
    $limit: Int = 20
    $offset: Int = 0
    $status: CustomerStatusEnum
    $search: String
  ) {
    customers(
      limit: $limit
      offset: $offset
      status: $status
      search: $search
      includeActivities: false
      includeNotes: false
    ) {
      customers {
        id
        customerNumber
        firstName
        lastName
        companyName
        email
        phone
        status
        customerType
        tier
        lifetimeValue
        totalPurchases
        lastContactDate
        createdAt
      }
      totalCount
      hasNextPage
    }
    customerMetrics {
      totalCustomers
      activeCustomers
      newCustomers
      churnedCustomers
      totalCustomerValue
      averageCustomerValue
    }
  }
`,(0,L.Ps)`
  query CustomerSubscriptions($customerId: ID!, $status: String, $limit: Int = 50) {
    customerSubscriptions(customerId: $customerId, status: $status, limit: $limit) {
      id
      subscriptionId
      customerId
      planId
      tenantId
      currentPeriodStart
      currentPeriodEnd
      status
      trialEnd
      isInTrial
      cancelAtPeriodEnd
      canceledAt
      endedAt
      createdAt
      updatedAt
    }
  }
`,(0,L.Ps)`
  query CustomerNetworkInfo($customerId: ID!) {
    customerNetworkInfo(customerId: $customerId)
  }
`,(0,L.Ps)`
  query CustomerDevices($customerId: ID!, $deviceType: String, $activeOnly: Boolean = true) {
    customerDevices(customerId: $customerId, deviceType: $deviceType, activeOnly: $activeOnly)
  }
`,(0,L.Ps)`
  query CustomerTickets($customerId: ID!, $limit: Int = 50, $status: String) {
    customerTickets(customerId: $customerId, limit: $limit, status: $status)
  }
`,(0,L.Ps)`
  query CustomerBilling(
    $customerId: ID!
    $includeInvoices: Boolean = true
    $invoiceLimit: Int = 50
  ) {
    customerBilling(
      customerId: $customerId
      includeInvoices: $includeInvoices
      invoiceLimit: $invoiceLimit
    )
  }
`,(0,L.Ps)`
  query Customer360View($customerId: ID!) {
    customer(id: $customerId, includeActivities: true, includeNotes: true) {
      id
      customerNumber
      firstName
      lastName
      middleName
      displayName
      companyName
      status
      customerType
      tier
      email
      emailVerified
      phone
      phoneVerified
      mobile
      addressLine1
      addressLine2
      city
      stateProvince
      postalCode
      country
      taxId
      industry
      employeeCount
      lifetimeValue
      totalPurchases
      averageOrderValue
      lastPurchaseDate
      createdAt
      updatedAt
      acquisitionDate
      lastContactDate
      activities {
        id
        customerId
        activityType
        title
        description
        performedBy
        createdAt
      }
      notes {
        id
        customerId
        subject
        content
        isInternal
        createdById
        createdAt
        updatedAt
      }
    }
    customerSubscriptions(customerId: $customerId, limit: 10) {
      id
      subscriptionId
      customerId
      planId
      status
      currentPeriodStart
      currentPeriodEnd
      isInTrial
      cancelAtPeriodEnd
      createdAt
    }
    customerNetworkInfo(customerId: $customerId)
    customerDevices(customerId: $customerId, activeOnly: true)
    customerTickets(customerId: $customerId, limit: 10)
    customerBilling(customerId: $customerId, includeInvoices: true, invoiceLimit: 10)
  }
`,(0,L.Ps)`
  subscription CustomerNetworkStatusUpdated($customerId: ID!) {
    customerNetworkStatusUpdated(customerId: $customerId) {
      customerId
      connectionStatus
      lastSeenAt
      ipv4Address
      ipv6Address
      macAddress
      vlanId
      signalStrength
      signalQuality
      uptimeSeconds
      uptimePercentage
      bandwidthUsageMbps
      downloadSpeedMbps
      uploadSpeedMbps
      packetLoss
      latencyMs
      jitter
      ontRxPower
      ontTxPower
      oltRxPower
      serviceStatus
      updatedAt
    }
  }
`,(0,L.Ps)`
  subscription CustomerDevicesUpdated($customerId: ID!) {
    customerDevicesUpdated(customerId: $customerId) {
      customerId
      deviceId
      deviceType
      deviceName
      status
      healthStatus
      isOnline
      lastSeenAt
      signalStrength
      temperature
      cpuUsage
      memoryUsage
      uptimeSeconds
      firmwareVersion
      needsFirmwareUpdate
      changeType
      previousValue
      newValue
      updatedAt
    }
  }
`,(0,L.Ps)`
  subscription CustomerTicketUpdated($customerId: ID!) {
    customerTicketUpdated(customerId: $customerId) {
      customerId
      action
      ticket {
        id
        ticketNumber
        title
        description
        status
        priority
        category
        subCategory
        assignedTo
        assignedToName
        assignedTeam
        createdAt
        updatedAt
        resolvedAt
        closedAt
        customerId
        customerName
      }
      changedBy
      changedByName
      changes
      comment
      updatedAt
    }
  }
`,(0,L.Ps)`
  subscription CustomerActivityAdded($customerId: ID!) {
    customerActivityAdded(customerId: $customerId) {
      id
      customerId
      activityType
      title
      description
      performedBy
      performedByName
      createdAt
    }
  }
`,(0,L.Ps)`
  subscription CustomerNoteUpdated($customerId: ID!) {
    customerNoteUpdated(customerId: $customerId) {
      customerId
      action
      note {
        id
        customerId
        subject
        content
        isInternal
        createdById
        createdByName
        createdAt
        updatedAt
      }
      changedBy
      changedByName
      updatedAt
    }
  }
`;let w=(0,L.Ps)`
  query FiberCableList(
    $limit: Int = 50
    $offset: Int = 0
    $status: FiberCableStatus
    $fiberType: FiberType
    $installationType: CableInstallationType
    $siteId: String
    $search: String
  ) {
    fiberCables(
      limit: $limit
      offset: $offset
      status: $status
      fiberType: $fiberType
      installationType: $installationType
      siteId: $siteId
      search: $search
    ) {
      cables {
        id
        cableId
        name
        description
        status
        isActive
        fiberType
        totalStrands
        availableStrands
        usedStrands
        manufacturer
        model
        installationType
        route {
          totalDistanceMeters
          startPoint {
            latitude
            longitude
            altitude
          }
          endPoint {
            latitude
            longitude
            altitude
          }
        }
        lengthMeters
        startDistributionPointId
        endDistributionPointId
        startPointName
        endPointName
        capacityUtilizationPercent
        bandwidthCapacityGbps
        spliceCount
        totalLossDb
        averageAttenuationDbPerKm
        maxAttenuationDbPerKm
        isLeased
        installedAt
        createdAt
        updatedAt
      }
      totalCount
      hasNextPage
    }
  }
`;function z(e){let t={...q,...e};return O.aM(w,t)}let x=(0,L.Ps)`
  query FiberCableDetail($id: ID!) {
    fiberCable(id: $id) {
      id
      cableId
      name
      description
      status
      isActive
      fiberType
      totalStrands
      availableStrands
      usedStrands
      manufacturer
      model
      installationType
      route {
        pathGeojson
        totalDistanceMeters
        startPoint {
          latitude
          longitude
          altitude
        }
        endPoint {
          latitude
          longitude
          altitude
        }
        intermediatePoints {
          latitude
          longitude
          altitude
        }
        elevationChangeMeters
        undergroundDistanceMeters
        aerialDistanceMeters
      }
      lengthMeters
      strands {
        strandId
        colorCode
        isActive
        isAvailable
        customerId
        customerName
        serviceId
        attenuationDb
        lossDb
        spliceCount
      }
      startDistributionPointId
      endDistributionPointId
      startPointName
      endPointName
      capacityUtilizationPercent
      bandwidthCapacityGbps
      splicePointIds
      spliceCount
      totalLossDb
      averageAttenuationDbPerKm
      maxAttenuationDbPerKm
      conduitId
      ductNumber
      armored
      fireRated
      ownerId
      ownerName
      isLeased
      installedAt
      testedAt
      createdAt
      updatedAt
    }
  }
`;function k(e){let t={...q,...e};return O.aM(x,t)}(0,L.Ps)`
  query FiberCablesByRoute($startPointId: String!, $endPointId: String!) {
    fiberCablesByRoute(startPointId: $startPointId, endPointId: $endPointId) {
      id
      cableId
      name
      status
      totalStrands
      availableStrands
      lengthMeters
      capacityUtilizationPercent
    }
  }
`,(0,L.Ps)`
  query FiberCablesByDistributionPoint($distributionPointId: String!) {
    fiberCablesByDistributionPoint(distributionPointId: $distributionPointId) {
      id
      cableId
      name
      status
      totalStrands
      availableStrands
      lengthMeters
    }
  }
`,(0,L.Ps)`
  query SplicePointList(
    $limit: Int = 50
    $offset: Int = 0
    $status: SpliceStatus
    $cableId: String
    $distributionPointId: String
  ) {
    splicePoints(
      limit: $limit
      offset: $offset
      status: $status
      cableId: $cableId
      distributionPointId: $distributionPointId
    ) {
      splicePoints {
        id
        spliceId
        cableId
        name
        description
        status
        isActive
        location {
          latitude
          longitude
          altitude
        }
        closureType
        manufacturer
        model
        trayCount
        trayCapacity
        cablesConnected
        cableCount
        totalSplices
        activeSplices
        averageSpliceLossDb
        maxSpliceLossDb
        passingSplices
        failingSplices
        accessType
        requiresSpecialAccess
        installedAt
        lastTestedAt
        lastMaintainedAt
        createdAt
        updatedAt
      }
      totalCount
      hasNextPage
    }
  }
`,(0,L.Ps)`
  query SplicePointDetail($id: ID!) {
    splicePoint(id: $id) {
      id
      spliceId
      name
      description
      status
      isActive
      location {
        latitude
        longitude
        altitude
      }
      address {
        streetAddress
        city
        stateProvince
        postalCode
        country
      }
      distributionPointId
      closureType
      manufacturer
      model
      trayCount
      trayCapacity
      cablesConnected
      cableCount
      spliceConnections {
        cableAId
        cableAStrand
        cableBId
        cableBStrand
        spliceType
        lossDb
        reflectanceDb
        isPassing
        testResult
        testedAt
        testedBy
      }
      totalSplices
      activeSplices
      averageSpliceLossDb
      maxSpliceLossDb
      passingSplices
      failingSplices
      accessType
      requiresSpecialAccess
      accessNotes
      installedAt
      lastTestedAt
      lastMaintainedAt
      createdAt
      updatedAt
    }
  }
`;let F=(0,L.Ps)`
  query SplicePointsByCable($cableId: String!) {
    splicePointsByCable(cableId: $cableId) {
      id
      spliceId
      cableId
      name
      status
      totalSplices
      activeSplices
      averageSpliceLossDb
      passingSplices
    }
  }
`;function V(e){let t={...q,...e};return O.aM(F,t)}let G=(0,L.Ps)`
  query DistributionPointList(
    $limit: Int = 50
    $offset: Int = 0
    $pointType: DistributionPointType
    $status: FiberCableStatus
    $siteId: String
    $nearCapacity: Boolean
  ) {
    distributionPoints(
      limit: $limit
      offset: $offset
      pointType: $pointType
      status: $status
      siteId: $siteId
      nearCapacity: $nearCapacity
    ) {
      distributionPoints {
        id
        siteId
        name
        description
        pointType
        status
        isActive
        location {
          latitude
          longitude
          altitude
        }
        manufacturer
        model
        totalCapacity
        availableCapacity
        usedCapacity
        portCount
        incomingCables
        outgoingCables
        totalCablesConnected
        splicePointCount
        hasPower
        batteryBackup
        environmentalMonitoring
        temperatureCelsius
        humidityPercent
        capacityUtilizationPercent
        fiberStrandCount
        availableStrandCount
        servesCustomerCount
        accessType
        requiresKey
        installedAt
        lastInspectedAt
        lastMaintainedAt
        createdAt
        updatedAt
      }
      totalCount
      hasNextPage
    }
  }
`;function _(e){let t={...q,...e};return O.aM(G,t)}(0,L.Ps)`
  query DistributionPointDetail($id: ID!) {
    distributionPoint(id: $id) {
      id
      siteId
      name
      description
      pointType
      status
      isActive
      location {
        latitude
        longitude
        altitude
      }
      address {
        streetAddress
        city
        stateProvince
        postalCode
        country
      }
      siteName
      manufacturer
      model
      totalCapacity
      availableCapacity
      usedCapacity
      ports {
        portNumber
        isAllocated
        isActive
        cableId
        strandId
        customerId
        customerName
        serviceId
      }
      portCount
      incomingCables
      outgoingCables
      totalCablesConnected
      splicePoints
      splicePointCount
      hasPower
      batteryBackup
      environmentalMonitoring
      temperatureCelsius
      humidityPercent
      capacityUtilizationPercent
      fiberStrandCount
      availableStrandCount
      serviceAreaIds
      servesCustomerCount
      accessType
      requiresKey
      securityLevel
      accessNotes
      installedAt
      lastInspectedAt
      lastMaintainedAt
      createdAt
      updatedAt
    }
  }
`,(0,L.Ps)`
  query DistributionPointsBySite($siteId: String!) {
    distributionPointsBySite(siteId: $siteId) {
      id
      siteId
      name
      pointType
      status
      totalCapacity
      availableCapacity
      capacityUtilizationPercent
      totalCablesConnected
      servesCustomerCount
    }
  }
`;let W=(0,L.Ps)`
  query ServiceAreaList(
    $limit: Int = 50
    $offset: Int = 0
    $areaType: ServiceAreaType
    $isServiceable: Boolean
    $constructionStatus: String
  ) {
    serviceAreas(
      limit: $limit
      offset: $offset
      areaType: $areaType
      isServiceable: $isServiceable
      constructionStatus: $constructionStatus
    ) {
      serviceAreas {
        id
        areaId
        name
        description
        areaType
        isActive
        isServiceable
        boundaryGeojson
        areaSqkm
        city
        stateProvince
        postalCodes
        streetCount
        homesPassed
        homesConnected
        businessesPassed
        businessesConnected
        penetrationRatePercent
        distributionPointCount
        totalFiberKm
        totalCapacity
        usedCapacity
        availableCapacity
        capacityUtilizationPercent
        maxBandwidthGbps
        estimatedPopulation
        householdDensityPerSqkm
        constructionStatus
        constructionCompletePercent
        targetCompletionDate
        plannedAt
        constructionStartedAt
        activatedAt
        createdAt
        updatedAt
      }
      totalCount
      hasNextPage
    }
  }
`;function H(e){let t={...q,...e};return O.aM(W,t)}(0,L.Ps)`
  query ServiceAreaDetail($id: ID!) {
    serviceArea(id: $id) {
      id
      areaId
      name
      description
      areaType
      isActive
      isServiceable
      boundaryGeojson
      areaSqkm
      city
      stateProvince
      postalCodes
      streetCount
      homesPassed
      homesConnected
      businessesPassed
      businessesConnected
      penetrationRatePercent
      distributionPointIds
      distributionPointCount
      totalFiberKm
      totalCapacity
      usedCapacity
      availableCapacity
      capacityUtilizationPercent
      maxBandwidthGbps
      averageDistanceToDistributionMeters
      estimatedPopulation
      householdDensityPerSqkm
      constructionStatus
      constructionCompletePercent
      targetCompletionDate
      plannedAt
      constructionStartedAt
      activatedAt
      createdAt
      updatedAt
    }
  }
`,(0,L.Ps)`
  query ServiceAreasByPostalCode($postalCode: String!) {
    serviceAreasByPostalCode(postalCode: $postalCode) {
      id
      areaId
      name
      city
      stateProvince
      isServiceable
      postalCodes
      homesPassed
      homesConnected
      penetrationRatePercent
      maxBandwidthGbps
    }
  }
`;let K=(0,L.Ps)`
  query FiberHealthMetrics($cableId: String, $healthStatus: FiberHealthStatus) {
    fiberHealthMetrics(cableId: $cableId, healthStatus: $healthStatus) {
      cableId
      cableName
      healthStatus
      healthScore
      totalLossDb
      averageLossPerKmDb
      maxLossPerKmDb
      reflectanceDb
      averageSpliceLossDb
      maxSpliceLossDb
      failingSplicesCount
      totalStrands
      activeStrands
      degradedStrands
      failedStrands
      lastTestedAt
      testPassRatePercent
      daysSinceLastTest
      activeAlarms
      warningCount
      requiresMaintenance
    }
  }
`;function j(e){let t={...q,...e};return O.aM(K,t)}(0,L.Ps)`
  query OTDRTestResults($cableId: String!, $strandId: Int, $limit: Int = 10) {
    otdrTestResults(cableId: $cableId, strandId: $strandId, limit: $limit) {
      testId
      cableId
      strandId
      testedAt
      testedBy
      wavelengthNm
      pulseWidthNs
      totalLossDb
      totalLengthMeters
      averageAttenuationDbPerKm
      spliceCount
      connectorCount
      bendCount
      breakCount
      isPassing
      passThresholdDb
      marginDb
      traceFileUrl
    }
  }
`,(0,L.Ps)`
  query FiberNetworkAnalytics {
    fiberNetworkAnalytics {
      totalFiberKm
      totalCables
      totalStrands
      totalDistributionPoints
      totalSplicePoints
      totalCapacity
      usedCapacity
      availableCapacity
      capacityUtilizationPercent
      cablesByStatus
      cablesByType
      healthyCables
      degradedCables
      failedCables
      networkHealthScore
      totalServiceAreas
      activeServiceAreas
      homesPassed
      homesConnected
      penetrationRatePercent
      averageCableLossDbPerKm
      averageSpliceLossDb
      cablesDueForTesting
      cablesActive
      cablesInactive
      cablesUnderConstruction
      cablesMaintenance
      cablesWithHighLoss
      distributionPointsNearCapacity
      serviceAreasNeedsExpansion
      generatedAt
    }
  }
`;let Q=(0,L.Ps)`
  query FiberDashboard {
    fiberDashboard {
      analytics {
        totalFiberKm
        totalCables
        totalStrands
        totalDistributionPoints
        totalSplicePoints
        capacityUtilizationPercent
        networkHealthScore
        homesPassed
        homesConnected
        penetrationRatePercent
      }
      topCablesByUtilization {
        id
        cableId
        name
        capacityUtilizationPercent
        totalStrands
        usedStrands
      }
      topDistributionPointsByCapacity {
        id
        name
        capacityUtilizationPercent
        totalCapacity
        usedCapacity
      }
      topServiceAreasByPenetration {
        id
        name
        city
        penetrationRatePercent
        homesPassed
        homesConnected
      }
      cablesRequiringAttention {
        id
        cableId
        cableName
        healthStatus
        healthScore
        requiresMaintenance
      }
      recentTestResults {
        testId
        cableId
        strandId
        testedAt
        isPassing
        totalLossDb
      }
      distributionPointsNearCapacity {
        id
        name
        capacityUtilizationPercent
      }
      serviceAreasExpansionCandidates {
        id
        name
        penetrationRatePercent
        homesPassed
      }
      newConnectionsTrend
      capacityUtilizationTrend
      networkHealthTrend
      generatedAt
    }
  }
`;function Y(e){let t={...q,...e};return O.aM(Q,t)}let Z=(0,L.Ps)`
  query NetworkOverview {
    networkOverview {
      totalDevices
      onlineDevices
      offlineDevices
      activeAlerts
      criticalAlerts
      totalBandwidthGbps
      uptimePercentage
      deviceTypeSummary {
        deviceType
        totalCount
        onlineCount
        avgCpuUsage
        avgMemoryUsage
      }
      recentAlerts {
        alertId
        severity
        title
        description
        deviceName
        deviceId
        deviceType
        triggeredAt
        acknowledgedAt
        resolvedAt
        isActive
      }
    }
  }
`;function X(e){let t={...q,...e};return O.aM(Z,t)}let J=(0,L.Ps)`
  query NetworkDeviceList(
    $page: Int = 1
    $pageSize: Int = 20
    $deviceType: DeviceTypeEnum
    $status: DeviceStatusEnum
    $search: String
  ) {
    networkDevices(
      page: $page
      pageSize: $pageSize
      deviceType: $deviceType
      status: $status
      search: $search
    ) {
      devices {
        deviceId
        deviceName
        deviceType
        status
        ipAddress
        firmwareVersion
        model
        location
        tenantId
        cpuUsagePercent
        memoryUsagePercent
        temperatureCelsius
        powerStatus
        pingLatencyMs
        packetLossPercent
        uptimeSeconds
        uptimeDays
        lastSeen
        isHealthy
      }
      totalCount
      hasNextPage
      hasPrevPage
      page
      pageSize
    }
  }
`;function ee(e){let t={...q,...e};return O.aM(J,t)}let et=(0,L.Ps)`
  query DeviceDetail($deviceId: String!, $deviceType: DeviceTypeEnum!) {
    deviceHealth(deviceId: $deviceId, deviceType: $deviceType) {
      deviceId
      deviceName
      deviceType
      status
      ipAddress
      firmwareVersion
      model
      location
      tenantId
      cpuUsagePercent
      memoryUsagePercent
      temperatureCelsius
      powerStatus
      pingLatencyMs
      packetLossPercent
      uptimeSeconds
      uptimeDays
      lastSeen
      isHealthy
    }
    deviceTraffic(deviceId: $deviceId, deviceType: $deviceType) {
      deviceId
      deviceName
      totalBandwidthGbps
      currentRateInMbps
      currentRateOutMbps
      totalBytesIn
      totalBytesOut
      totalPacketsIn
      totalPacketsOut
      peakRateInBps
      peakRateOutBps
      peakTimestamp
      timestamp
    }
  }
`;function ei(e){let t={...q,...e};return O.aM(et,t)}let es=(0,L.Ps)`
  query DeviceTraffic(
    $deviceId: String!
    $deviceType: DeviceTypeEnum!
    $includeInterfaces: Boolean = false
  ) {
    deviceTraffic(
      deviceId: $deviceId
      deviceType: $deviceType
      includeInterfaces: $includeInterfaces
    ) {
      deviceId
      deviceName
      totalBandwidthGbps
      currentRateInMbps
      currentRateOutMbps
      totalBytesIn
      totalBytesOut
      totalPacketsIn
      totalPacketsOut
      peakRateInBps
      peakRateOutBps
      peakTimestamp
      timestamp
      interfaces @include(if: $includeInterfaces) {
        interfaceName
        status
        rateInBps
        rateOutBps
        bytesIn
        bytesOut
        errorsIn
        errorsOut
        dropsIn
        dropsOut
      }
    }
  }
`;function ea(e){let t={...q,...e};return O.aM(es,t)}let en=(0,L.Ps)`
  query NetworkAlertList(
    $page: Int = 1
    $pageSize: Int = 50
    $severity: AlertSeverityEnum
    $activeOnly: Boolean = true
    $deviceId: String
    $deviceType: DeviceTypeEnum
  ) {
    networkAlerts(
      page: $page
      pageSize: $pageSize
      severity: $severity
      activeOnly: $activeOnly
      deviceId: $deviceId
      deviceType: $deviceType
    ) {
      alerts {
        alertId
        alertRuleId
        severity
        title
        description
        deviceName
        deviceId
        deviceType
        metricName
        currentValue
        thresholdValue
        triggeredAt
        acknowledgedAt
        resolvedAt
        isActive
        isAcknowledged
        tenantId
      }
      totalCount
      hasNextPage
      hasPrevPage
      page
      pageSize
    }
  }
`;function er(e){let t={...q,...e};return O.aM(en,t)}let ec=(0,L.Ps)`
  query NetworkAlertDetail($alertId: String!) {
    networkAlert(alertId: $alertId) {
      alertId
      alertRuleId
      severity
      title
      description
      deviceName
      deviceId
      deviceType
      metricName
      currentValue
      thresholdValue
      triggeredAt
      acknowledgedAt
      resolvedAt
      isActive
      isAcknowledged
      tenantId
    }
  }
`;function eo(e){let t={...q,...e};return O.aM(ec,t)}let ed=(0,L.Ps)`
  query NetworkDashboard(
    $devicePage: Int = 1
    $devicePageSize: Int = 10
    $deviceType: DeviceTypeEnum
    $deviceStatus: DeviceStatusEnum
    $alertPage: Int = 1
    $alertPageSize: Int = 20
    $alertSeverity: AlertSeverityEnum
  ) {
    networkOverview {
      totalDevices
      onlineDevices
      offlineDevices
      activeAlerts
      criticalAlerts
      totalBandwidthGbps
      uptimePercentage
      deviceTypeSummary {
        deviceType
        totalCount
        onlineCount
        avgCpuUsage
        avgMemoryUsage
      }
      recentAlerts {
        alertId
        severity
        title
        deviceName
        triggeredAt
        isActive
      }
    }
    networkDevices(
      page: $devicePage
      pageSize: $devicePageSize
      deviceType: $deviceType
      status: $deviceStatus
    ) {
      devices {
        deviceId
        deviceName
        deviceType
        status
        ipAddress
        cpuUsagePercent
        memoryUsagePercent
        uptimeSeconds
        isHealthy
        lastSeen
      }
      totalCount
      hasNextPage
    }
    networkAlerts(
      page: $alertPage
      pageSize: $alertPageSize
      severity: $alertSeverity
      activeOnly: true
    ) {
      alerts {
        alertId
        severity
        title
        description
        deviceName
        deviceType
        triggeredAt
        isActive
      }
      totalCount
      hasNextPage
    }
  }
`;function el(e){let t={...q,...e};return O.aM(ed,t)}(0,L.Ps)`
  subscription DeviceUpdates($deviceType: DeviceTypeEnum, $status: DeviceStatusEnum) {
    deviceUpdated(deviceType: $deviceType, status: $status) {
      deviceId
      deviceName
      deviceType
      status
      ipAddress
      firmwareVersion
      model
      location
      tenantId
      cpuUsagePercent
      memoryUsagePercent
      temperatureCelsius
      powerStatus
      pingLatencyMs
      packetLossPercent
      uptimeSeconds
      uptimeDays
      lastSeen
      isHealthy
      changeType
      previousValue
      newValue
      updatedAt
    }
  }
`,(0,L.Ps)`
  subscription NetworkAlertUpdates($severity: AlertSeverityEnum, $deviceId: String) {
    networkAlertUpdated(severity: $severity, deviceId: $deviceId) {
      action
      alert {
        alertId
        alertRuleId
        severity
        title
        description
        deviceName
        deviceId
        deviceType
        metricName
        currentValue
        thresholdValue
        triggeredAt
        acknowledgedAt
        resolvedAt
        isActive
        isAcknowledged
        tenantId
      }
      updatedAt
    }
  }
`;let eu=(0,L.Ps)`
  query SubscriberDashboard($limit: Int = 50, $search: String) {
    subscribers(limit: $limit, search: $search) {
      id
      subscriberId
      username
      enabled
      framedIpAddress
      bandwidthProfileId
      createdAt
      updatedAt
      sessions {
        radacctid
        username
        nasipaddress
        acctsessionid
        acctsessiontime
        acctinputoctets
        acctoutputoctets
        acctstarttime
      }
    }
    subscriberMetrics {
      totalCount
      enabledCount
      disabledCount
      activeSessionsCount
      totalDataUsageMb
    }
  }
`;function em(e){let t={...q,...e};return O.aM(eu,t)}(0,L.Ps)`
  query Subscriber($username: String!) {
    subscribers(limit: 1, search: $username) {
      id
      subscriberId
      username
      enabled
      framedIpAddress
      bandwidthProfileId
      createdAt
      updatedAt
      sessions {
        radacctid
        username
        nasipaddress
        acctsessionid
        acctsessiontime
        acctinputoctets
        acctoutputoctets
        acctstarttime
        acctstoptime
      }
    }
  }
`,(0,L.Ps)`
  query ActiveSessions($limit: Int = 100, $username: String) {
    sessions(limit: $limit, username: $username) {
      radacctid
      username
      nasipaddress
      acctsessionid
      acctsessiontime
      acctinputoctets
      acctoutputoctets
      acctstarttime
    }
  }
`,(0,L.Ps)`
  query SubscriberMetrics {
    subscriberMetrics {
      totalCount
      enabledCount
      disabledCount
      activeSessionsCount
      totalDataUsageMb
    }
  }
`;let ep=(0,L.Ps)`
  query SubscriptionList(
    $page: Int = 1
    $pageSize: Int = 10
    $status: SubscriptionStatusEnum
    $billingCycle: BillingCycleEnum
    $search: String
    $includeCustomer: Boolean = true
    $includePlan: Boolean = true
    $includeInvoices: Boolean = false
  ) {
    subscriptions(
      page: $page
      pageSize: $pageSize
      status: $status
      billingCycle: $billingCycle
      search: $search
      includeCustomer: $includeCustomer
      includePlan: $includePlan
      includeInvoices: $includeInvoices
    ) {
      subscriptions {
        id
        subscriptionId
        customerId
        planId
        tenantId
        currentPeriodStart
        currentPeriodEnd
        status
        trialEnd
        isInTrial
        cancelAtPeriodEnd
        canceledAt
        endedAt
        customPrice
        usageRecords
        createdAt
        updatedAt
        isActive
        daysUntilRenewal
        isPastDue
        customer @include(if: $includeCustomer) {
          id
          customerId
          name
          email
          phone
          createdAt
        }
        plan @include(if: $includePlan) {
          id
          planId
          productId
          name
          description
          billingCycle
          price
          currency
          setupFee
          trialDays
          isActive
          hasTrial
          hasSetupFee
          includedUsage
          overageRates
          createdAt
          updatedAt
        }
        recentInvoices @include(if: $includeInvoices) {
          id
          invoiceId
          invoiceNumber
          amount
          currency
          status
          dueDate
          paidAt
          createdAt
        }
      }
      totalCount
      hasNextPage
      hasPrevPage
      page
      pageSize
    }
  }
`;function eI(e){let t={...q,...e};return O.aM(ep,t)}let ey=(0,L.Ps)`
  query SubscriptionDetail($id: ID!) {
    subscription(id: $id, includeCustomer: true, includePlan: true, includeInvoices: true) {
      id
      subscriptionId
      customerId
      planId
      tenantId
      currentPeriodStart
      currentPeriodEnd
      status
      trialEnd
      isInTrial
      cancelAtPeriodEnd
      canceledAt
      endedAt
      customPrice
      usageRecords
      createdAt
      updatedAt
      isActive
      daysUntilRenewal
      isPastDue
      customer {
        id
        customerId
        name
        email
        phone
        createdAt
      }
      plan {
        id
        planId
        productId
        name
        description
        billingCycle
        price
        currency
        setupFee
        trialDays
        isActive
        hasTrial
        hasSetupFee
        includedUsage
        overageRates
        createdAt
        updatedAt
      }
      recentInvoices {
        id
        invoiceId
        invoiceNumber
        amount
        currency
        status
        dueDate
        paidAt
        createdAt
      }
    }
  }
`;function eg(e){let t={...q,...e};return O.aM(ey,t)}let eA=(0,L.Ps)`
  query SubscriptionMetrics {
    subscriptionMetrics {
      totalSubscriptions
      activeSubscriptions
      trialingSubscriptions
      pastDueSubscriptions
      canceledSubscriptions
      pausedSubscriptions
      monthlyRecurringRevenue
      annualRecurringRevenue
      averageRevenuePerUser
      newSubscriptionsThisMonth
      newSubscriptionsLastMonth
      churnRate
      growthRate
      monthlySubscriptions
      quarterlySubscriptions
      annualSubscriptions
      trialConversionRate
      activeTrials
    }
  }
`;function eP(e){let t={...q,...e};return O.aM(eA,t)}let ev=(0,L.Ps)`
  query PlanList(
    $page: Int = 1
    $pageSize: Int = 20
    $isActive: Boolean
    $billingCycle: BillingCycleEnum
  ) {
    plans(page: $page, pageSize: $pageSize, isActive: $isActive, billingCycle: $billingCycle) {
      plans {
        id
        planId
        productId
        name
        description
        billingCycle
        price
        currency
        setupFee
        trialDays
        isActive
        createdAt
        updatedAt
        hasTrial
        hasSetupFee
        includedUsage
        overageRates
      }
      totalCount
      hasNextPage
      hasPrevPage
      page
      pageSize
    }
  }
`;function eS(e){let t={...q,...e};return O.aM(ev,t)}let eb=(0,L.Ps)`
  query ProductList($page: Int = 1, $pageSize: Int = 20, $isActive: Boolean, $category: String) {
    products(page: $page, pageSize: $pageSize, isActive: $isActive, category: $category) {
      products {
        id
        productId
        sku
        name
        description
        category
        productType
        basePrice
        currency
        isActive
        createdAt
        updatedAt
      }
      totalCount
      hasNextPage
      hasPrevPage
      page
      pageSize
    }
  }
`;function eC(e){let t={...q,...e};return O.aM(eb,t)}let e$=(0,L.Ps)`
  query SubscriptionDashboard(
    $page: Int = 1
    $pageSize: Int = 10
    $status: SubscriptionStatusEnum
    $search: String
  ) {
    subscriptions(
      page: $page
      pageSize: $pageSize
      status: $status
      search: $search
      includeCustomer: true
      includePlan: true
      includeInvoices: false
    ) {
      subscriptions {
        id
        subscriptionId
        status
        currentPeriodStart
        currentPeriodEnd
        isActive
        isInTrial
        cancelAtPeriodEnd
        createdAt
        customer {
          id
          name
          email
        }
        plan {
          id
          name
          price
          currency
          billingCycle
        }
      }
      totalCount
      hasNextPage
    }
    subscriptionMetrics {
      totalSubscriptions
      activeSubscriptions
      trialingSubscriptions
      pastDueSubscriptions
      monthlyRecurringRevenue
      annualRecurringRevenue
      averageRevenuePerUser
      newSubscriptionsThisMonth
      churnRate
      growthRate
    }
  }
`;function eh(e){let t={...q,...e};return O.aM(e$,t)}(0,L.Ps)`
  query UserList(
    $page: Int = 1
    $pageSize: Int = 10
    $isActive: Boolean
    $isVerified: Boolean
    $isSuperuser: Boolean
    $isPlatformAdmin: Boolean
    $search: String
    $includeMetadata: Boolean = false
    $includeRoles: Boolean = false
    $includePermissions: Boolean = false
    $includeTeams: Boolean = false
  ) {
    users(
      page: $page
      pageSize: $pageSize
      isActive: $isActive
      isVerified: $isVerified
      isSuperuser: $isSuperuser
      isPlatformAdmin: $isPlatformAdmin
      search: $search
      includeMetadata: $includeMetadata
      includeRoles: $includeRoles
      includePermissions: $includePermissions
      includeTeams: $includeTeams
    ) {
      users {
        id
        username
        email
        fullName
        firstName
        lastName
        displayName
        isActive
        isVerified
        isSuperuser
        isPlatformAdmin
        status
        phoneNumber
        phone
        phoneVerified
        avatarUrl
        timezone
        location
        bio
        website
        mfaEnabled
        lastLogin
        lastLoginIp
        failedLoginAttempts
        lockedUntil
        language
        tenantId
        primaryRole
        createdAt
        updatedAt
        metadata @include(if: $includeMetadata)
        roles @include(if: $includeRoles) {
          id
          name
          displayName
          description
          priority
          isSystem
          isActive
          isDefault
          createdAt
          updatedAt
        }
        permissions @include(if: $includePermissions) {
          id
          name
          displayName
          description
          category
          isActive
          isSystem
          createdAt
          updatedAt
        }
        teams @include(if: $includeTeams) {
          teamId
          teamName
          role
          joinedAt
        }
      }
      totalCount
      hasNextPage
      hasPrevPage
      page
      pageSize
    }
  }
`,(0,L.Ps)`
  query UserDetail($id: ID!) {
    user(
      id: $id
      includeMetadata: true
      includeRoles: true
      includePermissions: true
      includeTeams: true
      includeProfileChanges: true
    ) {
      id
      username
      email
      fullName
      firstName
      lastName
      displayName
      isActive
      isVerified
      isSuperuser
      isPlatformAdmin
      status
      phoneNumber
      phone
      phoneVerified
      avatarUrl
      timezone
      location
      bio
      website
      mfaEnabled
      lastLogin
      lastLoginIp
      failedLoginAttempts
      lockedUntil
      language
      tenantId
      primaryRole
      createdAt
      updatedAt
      metadata
      roles {
        id
        name
        displayName
        description
        priority
        isSystem
        isActive
        isDefault
        createdAt
        updatedAt
      }
      permissions {
        id
        name
        displayName
        description
        category
        isActive
        isSystem
        createdAt
        updatedAt
      }
      teams {
        teamId
        teamName
        role
        joinedAt
      }
      profileChanges {
        id
        fieldName
        oldValue
        newValue
        createdAt
        changedByUsername
      }
    }
  }
`,(0,L.Ps)`
  query UserMetrics {
    userMetrics {
      totalUsers
      activeUsers
      suspendedUsers
      invitedUsers
      verifiedUsers
      mfaEnabledUsers
      platformAdmins
      superusers
      regularUsers
      usersLoggedInLast24h
      usersLoggedInLast7d
      usersLoggedInLast30d
      neverLoggedIn
      newUsersThisMonth
      newUsersLastMonth
    }
  }
`,(0,L.Ps)`
  query RoleList(
    $page: Int = 1
    $pageSize: Int = 20
    $isActive: Boolean
    $isSystem: Boolean
    $search: String
  ) {
    roles(
      page: $page
      pageSize: $pageSize
      isActive: $isActive
      isSystem: $isSystem
      search: $search
    ) {
      roles {
        id
        name
        displayName
        description
        priority
        isSystem
        isActive
        isDefault
        createdAt
        updatedAt
      }
      totalCount
      hasNextPage
      hasPrevPage
      page
      pageSize
    }
  }
`,(0,L.Ps)`
  query PermissionsByCategory($category: PermissionCategoryEnum) {
    permissionsByCategory(category: $category) {
      category
      count
      permissions {
        id
        name
        displayName
        description
        category
        isActive
        isSystem
        createdAt
        updatedAt
      }
    }
  }
`,(0,L.Ps)`
  query UserDashboard($page: Int = 1, $pageSize: Int = 10, $isActive: Boolean, $search: String) {
    users(
      page: $page
      pageSize: $pageSize
      isActive: $isActive
      search: $search
      includeMetadata: false
      includeRoles: true
      includePermissions: false
      includeTeams: false
    ) {
      users {
        id
        username
        email
        fullName
        isActive
        isVerified
        isSuperuser
        lastLogin
        createdAt
        roles {
          id
          name
          displayName
        }
      }
      totalCount
      hasNextPage
    }
    userMetrics {
      totalUsers
      activeUsers
      suspendedUsers
      verifiedUsers
      mfaEnabledUsers
      platformAdmins
      superusers
      regularUsers
      usersLoggedInLast24h
      usersLoggedInLast7d
      newUsersThisMonth
    }
  }
`,(0,L.Ps)`
  query UserRoles($id: ID!) {
    user(id: $id, includeRoles: true) {
      id
      username
      roles {
        id
        name
        displayName
        description
        priority
        isSystem
        isActive
        createdAt
      }
    }
  }
`,(0,L.Ps)`
  query UserPermissions($id: ID!) {
    user(id: $id, includePermissions: true) {
      id
      username
      permissions {
        id
        name
        displayName
        description
        category
        isActive
      }
    }
  }
`,(0,L.Ps)`
  query UserTeams($id: ID!) {
    user(id: $id, includeTeams: true) {
      id
      username
      teams {
        teamId
        teamName
        role
        joinedAt
      }
    }
  }
`;let ef=(0,L.Ps)`
  query AccessPointList(
    $limit: Int = 50
    $offset: Int = 0
    $siteId: String
    $status: AccessPointStatus
    $frequencyBand: FrequencyBand
    $search: String
  ) {
    accessPoints(
      limit: $limit
      offset: $offset
      siteId: $siteId
      status: $status
      frequencyBand: $frequencyBand
      search: $search
    ) {
      accessPoints {
        id
        name
        macAddress
        ipAddress
        serialNumber
        status
        isOnline
        lastSeenAt
        model
        manufacturer
        firmwareVersion
        ssid
        frequencyBand
        channel
        channelWidth
        transmitPower
        maxClients
        securityType
        location {
          siteName
          building
          floor
          room
          mountingType
          coordinates {
            latitude
            longitude
            altitude
          }
        }
        rfMetrics {
          signalStrengthDbm
          noiseFloorDbm
          signalToNoiseRatio
          channelUtilizationPercent
          interferenceLevel
          txPowerDbm
          rxPowerDbm
        }
        performance {
          txBytes
          rxBytes
          txPackets
          rxPackets
          txRateMbps
          rxRateMbps
          txErrors
          rxErrors
          connectedClients
          cpuUsagePercent
          memoryUsagePercent
          uptimeSeconds
        }
        siteId
        controllerName
        siteName
        createdAt
        updatedAt
        lastRebootAt
      }
      totalCount
      hasNextPage
    }
  }
`;function eD(e){let t={...q,...e};return O.aM(ef,t)}let eN=(0,L.Ps)`
  query AccessPointDetail($id: ID!) {
    accessPoint(id: $id) {
      id
      name
      macAddress
      ipAddress
      serialNumber
      status
      isOnline
      lastSeenAt
      model
      manufacturer
      firmwareVersion
      hardwareRevision
      ssid
      frequencyBand
      channel
      channelWidth
      transmitPower
      maxClients
      securityType
      location {
        siteName
        building
        floor
        room
        mountingType
        coordinates {
          latitude
          longitude
          altitude
          accuracy
        }
      }
      rfMetrics {
        signalStrengthDbm
        noiseFloorDbm
        signalToNoiseRatio
        channelUtilizationPercent
        interferenceLevel
        txPowerDbm
        rxPowerDbm
      }
      performance {
        txBytes
        rxBytes
        txPackets
        rxPackets
        txRateMbps
        rxRateMbps
        txErrors
        rxErrors
        txDropped
        rxDropped
        retries
        retryRatePercent
        connectedClients
        authenticatedClients
        authorizedClients
        cpuUsagePercent
        memoryUsagePercent
        uptimeSeconds
      }
      controllerId
      controllerName
      siteId
      siteName
      createdAt
      updatedAt
      lastRebootAt
      isMeshEnabled
      isBandSteeringEnabled
      isLoadBalancingEnabled
    }
  }
`;function eT(e){let t={...q,...e};return O.aM(eN,t)}(0,L.Ps)`
  query AccessPointsBySite($siteId: String!) {
    accessPointsBySite(siteId: $siteId) {
      id
      name
      macAddress
      ipAddress
      status
      isOnline
      ssid
      frequencyBand
      channel
      siteId
      siteName
      performance {
        connectedClients
        cpuUsagePercent
        memoryUsagePercent
      }
      rfMetrics {
        signalStrengthDbm
        channelUtilizationPercent
      }
    }
  }
`;let eE=(0,L.Ps)`
  query WirelessClientList(
    $limit: Int = 50
    $offset: Int = 0
    $accessPointId: String
    $customerId: String
    $frequencyBand: FrequencyBand
    $search: String
  ) {
    wirelessClients(
      limit: $limit
      offset: $offset
      accessPointId: $accessPointId
      customerId: $customerId
      frequencyBand: $frequencyBand
      search: $search
    ) {
      clients {
        id
        macAddress
        hostname
        ipAddress
        manufacturer
        accessPointId
        accessPointName
        ssid
        connectionType
        frequencyBand
        channel
        isAuthenticated
        isAuthorized
        signalStrengthDbm
        signalQuality {
          rssiDbm
          snrDb
          noiseFloorDbm
          signalStrengthPercent
          linkQualityPercent
        }
        noiseFloorDbm
        snr
        txRateMbps
        rxRateMbps
        txBytes
        rxBytes
        connectedAt
        lastSeenAt
        uptimeSeconds
        customerId
        customerName
      }
      totalCount
      hasNextPage
    }
  }
`;function eR(e){let t={...q,...e};return O.aM(eE,t)}(0,L.Ps)`
  query WirelessClientDetail($id: ID!) {
    wirelessClient(id: $id) {
      id
      macAddress
      hostname
      ipAddress
      manufacturer
      accessPointId
      accessPointName
      ssid
      connectionType
      frequencyBand
      channel
      isAuthenticated
      isAuthorized
      authMethod
      signalStrengthDbm
      signalQuality {
        rssiDbm
        snrDb
        noiseFloorDbm
        signalStrengthPercent
        linkQualityPercent
      }
      noiseFloorDbm
      snr
      txRateMbps
      rxRateMbps
      txBytes
      rxBytes
      txPackets
      rxPackets
      txRetries
      rxRetries
      connectedAt
      lastSeenAt
      uptimeSeconds
      idleTimeSeconds
      supports80211k
      supports80211r
      supports80211v
      maxPhyRateMbps
      customerId
      customerName
    }
  }
`;let eB=(0,L.Ps)`
  query WirelessClientsByAccessPoint($accessPointId: String!) {
    wirelessClientsByAccessPoint(accessPointId: $accessPointId) {
      id
      macAddress
      hostname
      ipAddress
      accessPointId
      ssid
      signalStrengthDbm
      signalQuality {
        rssiDbm
        snrDb
        noiseFloorDbm
        signalStrengthPercent
        linkQualityPercent
      }
      txRateMbps
      rxRateMbps
      connectedAt
      customerId
      customerName
    }
  }
`;function eM(e){let t={...q,...e};return O.aM(eB,t)}(0,L.Ps)`
  query WirelessClientsByCustomer($customerId: String!) {
    wirelessClientsByCustomer(customerId: $customerId) {
      id
      macAddress
      hostname
      ipAddress
      customerId
      accessPointName
      ssid
      frequencyBand
      signalStrengthDbm
      signalQuality {
        rssiDbm
        snrDb
        noiseFloorDbm
        signalStrengthPercent
        linkQualityPercent
      }
      isAuthenticated
      connectedAt
      lastSeenAt
    }
  }
`;let eU=(0,L.Ps)`
  query CoverageZoneList($limit: Int = 50, $offset: Int = 0, $siteId: String, $areaType: String) {
    coverageZones(limit: $limit, offset: $offset, siteId: $siteId, areaType: $areaType) {
      zones {
        id
        name
        description
        siteId
        siteName
        floor
        areaType
        coverageAreaSqm
        signalStrengthMinDbm
        signalStrengthMaxDbm
        signalStrengthAvgDbm
        accessPointIds
        accessPointCount
        interferenceLevel
        channelUtilizationAvg
        noiseFloorAvgDbm
        connectedClients
        maxClientCapacity
        clientDensityPerAp
        coveragePolygon
        createdAt
        updatedAt
        lastSurveyedAt
      }
      totalCount
      hasNextPage
    }
  }
`;function eL(e){let t={...q,...e};return O.aM(eU,t)}(0,L.Ps)`
  query CoverageZoneDetail($id: ID!) {
    coverageZone(id: $id) {
      id
      name
      description
      siteId
      siteName
      floor
      areaType
      coverageAreaSqm
      signalStrengthMinDbm
      signalStrengthMaxDbm
      signalStrengthAvgDbm
      accessPointIds
      accessPointCount
      interferenceLevel
      channelUtilizationAvg
      noiseFloorAvgDbm
      connectedClients
      maxClientCapacity
      clientDensityPerAp
      coveragePolygon
      createdAt
      updatedAt
      lastSurveyedAt
    }
  }
`,(0,L.Ps)`
  query CoverageZonesBySite($siteId: String!) {
    coverageZonesBySite(siteId: $siteId) {
      id
      name
      siteId
      siteName
      floor
      areaType
      coverageAreaSqm
      accessPointCount
      connectedClients
      maxClientCapacity
      signalStrengthAvgDbm
    }
  }
`;let eO=(0,L.Ps)`
  query RFAnalytics($siteId: String!) {
    rfAnalytics(siteId: $siteId) {
      siteId
      siteName
      analysisTimestamp
      channelUtilization24ghz {
        channel
        frequencyMhz
        band
        utilizationPercent
        interferenceLevel
        accessPointsCount
      }
      channelUtilization5ghz {
        channel
        frequencyMhz
        band
        utilizationPercent
        interferenceLevel
        accessPointsCount
      }
      channelUtilization6ghz {
        channel
        frequencyMhz
        band
        utilizationPercent
        interferenceLevel
        accessPointsCount
      }
      recommendedChannels24ghz
      recommendedChannels5ghz
      recommendedChannels6ghz
      interferenceSources {
        sourceType
        frequencyMhz
        strengthDbm
        affectedChannels
      }
      totalInterferenceScore
      averageSignalStrengthDbm
      averageSnr
      coverageQualityScore
      clientsPerBand24ghz
      clientsPerBand5ghz
      clientsPerBand6ghz
      bandUtilizationBalanceScore
    }
  }
`;function eq(e){let t={...q,...e};return O.aM(eO,t)}let ew=(0,L.Ps)`
  query ChannelUtilization($siteId: String!, $frequencyBand: FrequencyBand!) {
    channelUtilization(siteId: $siteId, frequencyBand: $frequencyBand) {
      channel
      frequencyMhz
      band
      utilizationPercent
      interferenceLevel
      accessPointsCount
    }
  }
`;function ez(e){let t={...q,...e};return O.aM(ew,t)}(0,L.Ps)`
  query WirelessSiteMetrics($siteId: String!) {
    wirelessSiteMetrics(siteId: $siteId) {
      siteId
      siteName
      totalAps
      onlineAps
      offlineAps
      degradedAps
      totalClients
      clients24ghz
      clients5ghz
      clients6ghz
      averageSignalStrengthDbm
      averageSnr
      totalThroughputMbps
      totalCapacity
      capacityUtilizationPercent
      overallHealthScore
      rfHealthScore
      clientExperienceScore
    }
  }
`;let ex=(0,L.Ps)`
  query WirelessDashboard {
    wirelessDashboard {
      totalSites
      totalAccessPoints
      totalClients
      totalCoverageZones
      onlineAps
      offlineAps
      degradedAps
      clientsByBand24ghz
      clientsByBand5ghz
      clientsByBand6ghz
      topApsByClients {
        id
        name
        siteName
        performance {
          connectedClients
        }
      }
      topApsByThroughput {
        id
        name
        siteName
        performance {
          txRateMbps
          rxRateMbps
        }
      }
      sitesWithIssues {
        siteId
        siteName
        offlineAps
        degradedAps
        overallHealthScore
      }
      totalThroughputMbps
      averageSignalStrengthDbm
      averageClientExperienceScore
      clientCountTrend
      throughputTrendMbps
      offlineEventsCount
      generatedAt
    }
  }
`;function ek(e){let t={...q,...e};return O.aM(ex,t)}}};