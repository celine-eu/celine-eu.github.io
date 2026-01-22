# CELINE Ontology

**Namespace**

`https://celine-eu.github.io/ontologies/celine#`

## Classes

- [Asset](#Asset)
- [Datapoint](#Datapoint)
- [EnergyCommunity](#EnergyCommunity)
- [FlexibilityRequest](#FlexibilityRequest)
- [Forecast](#Forecast)
- [KPIAssessment](#KPIAssessment)
- [Measurement](#Measurement)
- [Membership](#Membership)
- [Meter](#Meter)
- [ModelRun](#ModelRun)
- [Participant](#Participant)
- [Scenario](#Scenario)
- [Site](#Site)
- [Snapshot](#Snapshot)
- [Tariff](#Tariff)
- [TimeSeries](#TimeSeries)
- [WeatherObservation](#WeatherObservation)

## Properties

- [authURI](#authURI)
- [connectedTo](#connectedTo)
- [datasetURI](#datasetURI)
- [geoJSON](#geoJSON)
- [hasDatapoint](#hasDatapoint)
- [hasMember](#hasMember)
- [hasMembership](#hasMembership)
- [hasMeter](#hasMeter)
- [hasTariff](#hasTariff)
- [hasTimeSeries](#hasTimeSeries)
- [isMemberOf](#isMemberOf)
- [isOwnedBy](#isOwnedBy)
- [locatedAt](#locatedAt)
- [membershipCommunity](#membershipCommunity)
- [membershipParticipant](#membershipParticipant)
- [membershipRole](#membershipRole)
- [metric](#metric)
- [observedEntity](#observedEntity)
- [ownsAsset](#ownsAsset)
- [producedBy](#producedBy)
- [relatedToForecast](#relatedToForecast)
- [relatedToPOD](#relatedToPOD)
- [sensorId](#sensorId)
- [timestamp](#timestamp)
- [unit](#unit)
- [usesScenario](#usesScenario)
- [usesSnapshot](#usesSnapshot)
- [validFrom](#validFrom)
- [validTo](#validTo)
- [value](#value)
- [votingWeight](#votingWeight)

<a id="Asset"></a>
<a id="asset"></a>
## Asset

**IRI** `https://celine-eu.github.io/ontologies/celine#Asset`

**Label** Asset

**Description** A physical or logical energy asset (PV, battery, EVSE, load, meter, etc.). PECO defines the asset backbone; SAREF provides device semantics.

<a id="Datapoint"></a>
<a id="datapoint"></a>
## Datapoint

**IRI** `https://celine-eu.github.io/ontologies/celine#Datapoint`

**Label** Datapoint

**Description** A single time-value pair in a time series.

<a id="EnergyCommunity"></a>
<a id="energycommunity"></a>
## EnergyCommunity

**IRI** `https://celine-eu.github.io/ontologies/celine#EnergyCommunity`

**Label** Energy Community

**Description** A Renewable/Citizen Energy Community represented in CELINE. PECO provides the primary semantics; SAREF4CITY alignment is optional for smart city interoperability.

<a id="FlexibilityRequest"></a>
<a id="flexibilityrequest"></a>
## FlexibilityRequest

**IRI** `https://celine-eu.github.io/ontologies/celine#FlexibilityRequest`

**Label** Flexibility Request

**Description** A request or event describing flexibility needs/activation in the community.

<a id="Forecast"></a>
<a id="forecast"></a>
## Forecast

**IRI** `https://celine-eu.github.io/ontologies/celine#Forecast`

**Label** Forecast

**Description** A forecast represented as a time series, with provenance of the generating model/run.

<a id="KPIAssessment"></a>
<a id="kpiassessment"></a>
## KPIAssessment

**IRI** `https://celine-eu.github.io/ontologies/celine#KPIAssessment`

**Label** KPI Assessment

**Description** An assessment result for a KPI, typically derived from measurements/forecasts over a time window.

<a id="Measurement"></a>
<a id="measurement"></a>
## Measurement

**IRI** `https://celine-eu.github.io/ontologies/celine#Measurement`

**Label** Measurement

**Description** A measurement event or record. CELINE uses PECO Measurement for energy-domain measurement semantics.

<a id="Membership"></a>
<a id="membership"></a>
## Membership

**IRI** `https://celine-eu.github.io/ontologies/celine#Membership`

**Label** Membership

**Description** A membership record capturing a participant's role(s), weights and validity within a community.

<a id="Meter"></a>
<a id="meter"></a>
## Meter

**IRI** `https://celine-eu.github.io/ontologies/celine#Meter`

**Label** Meter

**Description** A metering point / point of delivery (POD) that may be associated with an EnergyMeter device.

<a id="ModelRun"></a>
<a id="modelrun"></a>
## ModelRun

**IRI** `https://celine-eu.github.io/ontologies/celine#ModelRun`

**Label** Model Run

**Description** An execution activity that generates forecasts, simulations, or KPI assessments from a snapshot and scenario.

<a id="Participant"></a>
<a id="participant"></a>
## Participant

**IRI** `https://celine-eu.github.io/ontologies/celine#Participant`

**Label** Participant

**Description** An actor participating in a community (individual, organisation, aggregator, operator). This is a thin alias over PECO Agent with PROV agent semantics.

<a id="Scenario"></a>
<a id="scenario"></a>
## Scenario

**IRI** `https://celine-eu.github.io/ontologies/celine#Scenario`

**Label** Scenario

**Description** A set of assumptions and overrides applied to a Snapshot for what-if analysis and digital twin runs.

<a id="Site"></a>
<a id="site"></a>
## Site

**IRI** `https://celine-eu.github.io/ontologies/celine#Site`

**Label** Site

**Description** A physical site relevant to a community (building, facility, or spatial container) where assets are located.

<a id="Snapshot"></a>
<a id="snapshot"></a>
## Snapshot

**IRI** `https://celine-eu.github.io/ontologies/celine#Snapshot`

**Label** Snapshot

**Description** A frozen, reproducible capture of the REC catalogue state and configuration used for computations (forecasting, simulation, KPI evaluation).

<a id="Tariff"></a>
<a id="tariff"></a>
## Tariff

**IRI** `https://celine-eu.github.io/ontologies/celine#Tariff`

**Label** Tariff

**Description** A tariff applicable to a community/member/asset for allocation, billing or settlement. Anchored in PECO and optionally aligned with BIGG tariff.

<a id="TimeSeries"></a>
<a id="timeseries"></a>
## TimeSeries

**IRI** `https://celine-eu.github.io/ontologies/celine#TimeSeries`

**Label** Time Series

**Description** A time series of datapoints (measured or forecast). CELINE adopts PECO Timeseries for efficient API representation.

<a id="WeatherObservation"></a>
<a id="weatherobservation"></a>
## WeatherObservation

**IRI** `https://celine-eu.github.io/ontologies/celine#WeatherObservation`

**Label** Weather Observation

**Description** An observation of a weather-related phenomenon (temperature, irradiance, wind, etc.), modelled using SOSA.

<a id="authURI"></a>
<a id="authuri"></a>
## authURI

**IRI** `https://celine-eu.github.io/ontologies/celine#authURI`

**Label** authentication URI

**Description** IRI/CURIE-expanded URI of the participant in the authentication/IdM system.

<a id="connectedTo"></a>
<a id="connectedto"></a>
## connectedTo

**IRI** `https://celine-eu.github.io/ontologies/celine#connectedTo`

**Label** connected to

**Description** Topological connection between two entities (e.g., meter connected to substation).

<a id="datasetURI"></a>
<a id="dataseturi"></a>
## datasetURI

**IRI** `https://celine-eu.github.io/ontologies/celine#datasetURI`

**Label** dataset URI

**Description** URI of the dataset resource where time series datapoints are stored/queried.

<a id="geoJSON"></a>
<a id="geojson"></a>
## geoJSON

**IRI** `https://celine-eu.github.io/ontologies/celine#geoJSON`

**Label** GeoJSON geometry

**Description** GeoJSON geometry (WGS84; coordinates in lon/lat order) for consistent geospatial positioning.

<a id="hasDatapoint"></a>
<a id="hasdatapoint"></a>
## hasDatapoint

**IRI** `https://celine-eu.github.io/ontologies/celine#hasDatapoint`

**Label** has datapoint

**Description** Associates a time series with its datapoints. Alias of peco:has_datapoint.

<a id="hasMember"></a>
<a id="hasmember"></a>
## hasMember

**IRI** `https://celine-eu.github.io/ontologies/celine#hasMember`

**Label** has member

**Description** Links a community to a participant that is a member of the community. Alias of peco:has_member.

<a id="hasMembership"></a>
<a id="hasmembership"></a>
## hasMembership

**IRI** `https://celine-eu.github.io/ontologies/celine#hasMembership`

**Label** has membership

**Description** Links a community to membership records (role, weights, validity).

<a id="hasMeter"></a>
<a id="hasmeter"></a>
## hasMeter

**IRI** `https://celine-eu.github.io/ontologies/celine#hasMeter`

**Label** has meter

**Description** Associates an asset or site with a metering point (POD / meter).

<a id="hasTariff"></a>
<a id="hastariff"></a>
## hasTariff

**IRI** `https://celine-eu.github.io/ontologies/celine#hasTariff`

**Label** has tariff

**Description** Associates a community, membership, POD or asset with a tariff. Alias of peco:has_tariff.

<a id="hasTimeSeries"></a>
<a id="hastimeseries"></a>
## hasTimeSeries

**IRI** `https://celine-eu.github.io/ontologies/celine#hasTimeSeries`

**Label** has time series

**Description** Associates an entity (asset, POD, KPI, forecast) with a time series.

<a id="isMemberOf"></a>
<a id="ismemberof"></a>
## isMemberOf

**IRI** `https://celine-eu.github.io/ontologies/celine#isMemberOf`

**Label** is member of

**Description** Links a participant to the community they are a member of. Alias of peco:is_member_of.

<a id="isOwnedBy"></a>
<a id="isownedby"></a>
## isOwnedBy

**IRI** `https://celine-eu.github.io/ontologies/celine#isOwnedBy`

**Label** is owned by

**Description** Links an asset to its owner participant. Alias of peco:is_owned_by.

<a id="locatedAt"></a>
<a id="locatedat"></a>
## locatedAt

**IRI** `https://celine-eu.github.io/ontologies/celine#locatedAt`

**Label** located at

**Description** Links an asset or POD to the site where it is located.

<a id="membershipCommunity"></a>
<a id="membershipcommunity"></a>
## membershipCommunity

**IRI** `https://celine-eu.github.io/ontologies/celine#membershipCommunity`

**Label** membership community

<a id="membershipParticipant"></a>
<a id="membershipparticipant"></a>
## membershipParticipant

**IRI** `https://celine-eu.github.io/ontologies/celine#membershipParticipant`

**Label** membership participant

<a id="membershipRole"></a>
<a id="membershiprole"></a>
## membershipRole

**IRI** `https://celine-eu.github.io/ontologies/celine#membershipRole`

**Label** membership role

**Description** Role of the participant within the community (e.g., consumer, prosumer, producer, operator).

<a id="metric"></a>
<a id="metric"></a>
## metric

**IRI** `https://celine-eu.github.io/ontologies/celine#metric`

**Label** metric

**Description** Identifier of the metric/phenomenon (e.g., active_power, energy, temperature, irradiance).

<a id="observedEntity"></a>
<a id="observedentity"></a>
## observedEntity

**IRI** `https://celine-eu.github.io/ontologies/celine#observedEntity`

**Label** observed entity

**Description** The entity that a time series / measurement refers to.

<a id="ownsAsset"></a>
<a id="ownsasset"></a>
## ownsAsset

**IRI** `https://celine-eu.github.io/ontologies/celine#ownsAsset`

**Label** owns asset

**Description** Links a participant to an owned asset. Alias of peco:owns.

<a id="producedBy"></a>
<a id="producedby"></a>
## producedBy

**IRI** `https://celine-eu.github.io/ontologies/celine#producedBy`

**Label** produced by

**Description** Links an entity (forecast/KPI) to the model run that generated it.

<a id="relatedToForecast"></a>
<a id="relatedtoforecast"></a>
## relatedToForecast

**IRI** `https://celine-eu.github.io/ontologies/celine#relatedToForecast`

**Label** related to forecast

**Description** Associates an entity to a forecast series. Alias of peco:related_to_forecast.

<a id="relatedToPOD"></a>
<a id="relatedtopod"></a>
## relatedToPOD

**IRI** `https://celine-eu.github.io/ontologies/celine#relatedToPOD`

**Label** related to POD

**Description** Associates a measurement/series with a POD. Alias of peco:related_to_pod.

<a id="sensorId"></a>
<a id="sensorid"></a>
## sensorId

**IRI** `https://celine-eu.github.io/ontologies/celine#sensorId`

**Label** sensor id

**Description** Non-PII sensor identifier used to filter metering datasets.

<a id="timestamp"></a>
<a id="timestamp"></a>
## timestamp

**IRI** `https://celine-eu.github.io/ontologies/celine#timestamp`

**Label** timestamp

**Description** Timestamp of a datapoint. Alias of peco:has_timestamp.

<a id="unit"></a>
<a id="unit"></a>
## unit

**IRI** `https://celine-eu.github.io/ontologies/celine#unit`

**Label** unit

**Description** Unit of measure (string code) used in APIs when a full unit ontology is not required.

<a id="usesScenario"></a>
<a id="usesscenario"></a>
## usesScenario

**IRI** `https://celine-eu.github.io/ontologies/celine#usesScenario`

**Label** uses scenario

**Description** Links a model run, forecast or KPI assessment to a scenario of assumptions/overrides.

<a id="usesSnapshot"></a>
<a id="usessnapshot"></a>
## usesSnapshot

**IRI** `https://celine-eu.github.io/ontologies/celine#usesSnapshot`

**Label** uses snapshot

**Description** Links a model run, forecast or KPI assessment to the snapshot it is based on.

<a id="validFrom"></a>
<a id="validfrom"></a>
## validFrom

**IRI** `https://celine-eu.github.io/ontologies/celine#validFrom`

**Label** valid from

<a id="validTo"></a>
<a id="validto"></a>
## validTo

**IRI** `https://celine-eu.github.io/ontologies/celine#validTo`

**Label** valid to

<a id="value"></a>
<a id="value"></a>
## value

**IRI** `https://celine-eu.github.io/ontologies/celine#value`

**Label** value

**Description** Numeric value of a datapoint. Alias of peco:has_value.

<a id="votingWeight"></a>
<a id="votingweight"></a>
## votingWeight

**IRI** `https://celine-eu.github.io/ontologies/celine#votingWeight`

**Label** voting weight

**Description** Optional voting weight or share used in governance.
