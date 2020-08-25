## Karbon Platform Services for IoT CLI

The data interfaces created as part of the following steps require the Karbon Platform Services for IoT CLI.  Open [cli](https://github.com/nutanix/xi-iot/tree/master/cli) in your browser and follow the steps to install the Karbon Platform Services for IoT CLI. 

## Registering a Data Sources

In Karbon Platform Services for IoT, data sources connect cloud entities such as Applications and Data Pipelines to edge devices. Support for configuring MQTT, RTSP, and GigE Vision data sources is built into the UI. 

Other data sources, called data interfaces,can be deployed using the Karbon Platform Services for IoT CLI. The CLI commands accept YAML input to specify criteria such as service domains and topics. 
The following examples assume you have installed and configured the CLI.

## Data Interfaces

Karbon Platform Services for IoT Data Interfaces are micro services (containers) that contain logic for connecting to virtually any external device or protocol. Data interfaces contain device & protocol drivers and any prerequisite components packaged into a lightweight container runtime alongside logic written to Karbon Platform Services for IoT API specifications for data exchange. 
