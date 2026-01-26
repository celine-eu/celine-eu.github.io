# CELINE Ontology

**Namespace**

`https://celine-eu.github.io/ontologies/celine#`

## Classes

- [CommunityContext](#CommunityContext)
- [DatasetReference](#DatasetReference)
- [KPIEvaluation](#KPIEvaluation)
- [Scenario](#Scenario)
- [Simulation](#Simulation)
- [SimulationRun](#SimulationRun)

## Properties

- [evaluatesKPI](#evaluatesKPI)
- [hasCommunity](#hasCommunity)
- [hasKPIEvaluation](#hasKPIEvaluation)
- [hasScenario](#hasScenario)
- [hasSimulation](#hasSimulation)
- [hasSimulationRun](#hasSimulationRun)
- [hasTimeInterval](#hasTimeInterval)
- [producesDataset](#producesDataset)
- [usesAsset](#usesAsset)
- [usesDataset](#usesDataset)
- [usesObservation](#usesObservation)

<a id="CommunityContext"></a>
<a id="communitycontext"></a>
## CommunityContext

**IRI** `https://w3id.org/celine/ontology#CommunityContext`

**Label** Community Context

**Description** 
    Operational context binding a PECO Energy Community
    with assets, datasets and simulations.
    

<a id="DatasetReference"></a>
<a id="datasetreference"></a>
## DatasetReference

**IRI** `https://w3id.org/celine/ontology#DatasetReference`

**Label** Dataset Reference

**Description** 
    Reference to an external dataset used as input or produced as output.
    CELINE does not define dataset schemas.
    

<a id="KPIEvaluation"></a>
<a id="kpievaluation"></a>
## KPIEvaluation

**IRI** `https://w3id.org/celine/ontology#KPIEvaluation`

**Label** KPI Evaluation

**Description** 
    Evaluation of a BIGG KPI in a specific Scenario or SimulationRun.
    

<a id="Scenario"></a>
<a id="scenario"></a>
## Scenario

**IRI** `https://w3id.org/celine/ontology#Scenario`

**Label** Scenario

**Description** 
    Definition of assumptions, temporal scope and configuration
    for one or more simulations.
    

<a id="Simulation"></a>
<a id="simulation"></a>
## Simulation

**IRI** `https://w3id.org/celine/ontology#Simulation`

**Label** Simulation

**Description** 
    Abstract simulation definition independent from execution.
    

<a id="SimulationRun"></a>
<a id="simulationrun"></a>
## SimulationRun

**IRI** `https://w3id.org/celine/ontology#SimulationRun`

**Label** Simulation Run

**Description** 
    Concrete execution of a Simulation under a specific Scenario.
    

<a id="evaluatesKPI"></a>
<a id="evaluateskpi"></a>
## evaluatesKPI

**IRI** `https://w3id.org/celine/ontology#evaluatesKPI`

**Label** evaluates KPI

<a id="hasCommunity"></a>
<a id="hascommunity"></a>
## hasCommunity

**IRI** `https://w3id.org/celine/ontology#hasCommunity`

**Label** has energy community

<a id="hasKPIEvaluation"></a>
<a id="haskpievaluation"></a>
## hasKPIEvaluation

**IRI** `https://w3id.org/celine/ontology#hasKPIEvaluation`

**Label** has KPI evaluation

<a id="hasScenario"></a>
<a id="hasscenario"></a>
## hasScenario

**IRI** `https://w3id.org/celine/ontology#hasScenario`

**Label** has scenario

<a id="hasSimulation"></a>
<a id="hassimulation"></a>
## hasSimulation

**IRI** `https://w3id.org/celine/ontology#hasSimulation`

**Label** has simulation

<a id="hasSimulationRun"></a>
<a id="hassimulationrun"></a>
## hasSimulationRun

**IRI** `https://w3id.org/celine/ontology#hasSimulationRun`

**Label** has simulation run

<a id="hasTimeInterval"></a>
<a id="hastimeinterval"></a>
## hasTimeInterval

**IRI** `https://w3id.org/celine/ontology#hasTimeInterval`

**Label** has time interval

<a id="producesDataset"></a>
<a id="producesdataset"></a>
## producesDataset

**IRI** `https://w3id.org/celine/ontology#producesDataset`

**Label** produces dataset

<a id="usesAsset"></a>
<a id="usesasset"></a>
## usesAsset

**IRI** `https://w3id.org/celine/ontology#usesAsset`

**Label** uses asset

**Description** References SAREF or SAREF4ENER devices.

<a id="usesDataset"></a>
<a id="usesdataset"></a>
## usesDataset

**IRI** `https://w3id.org/celine/ontology#usesDataset`

**Label** uses dataset

<a id="usesObservation"></a>
<a id="usesobservation"></a>
## usesObservation

**IRI** `https://w3id.org/celine/ontology#usesObservation`

**Label** uses observation

**Description** References SOSA observations (e.g. weather, sensors).
