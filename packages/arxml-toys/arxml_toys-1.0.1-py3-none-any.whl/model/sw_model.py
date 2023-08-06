''' SWC object '''

import xml.etree.ElementTree as ET
import re
from xml.etree.ElementTree import Element
from xml.dom import minidom
from typing import List, Set, Dict
from collections import OrderedDict

from enum import Enum

from matplotlib.pyplot import text

class Parameter:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.direction = ""
        self.position = 0

class Operation:
    def __init__(self, name: str):
        self.id = ""
        self.name = name
        self.return_type = ""
        self.note = ""
        self._parameters = {}

    #@property
    #def name(self) -> str:
    #    return self._name

    def addParameter(self, parameter: Parameter):
        if (parameter not in self._parameters):
            if (parameter.position == 0):
                parameter.position = len(self._parameters) + 1
            self._parameters[parameter.name] = parameter

    def getParameters(self) -> List[Parameter]:
        return sorted(self._parameters.values(), key=lambda p: p.position)

class DataElement:
    def __init__(self, name: str):
        self.name = name
        self.type = ""
        self.position = 0

class AbstractInterface:
    def __init__(self, name: str):
        self.name = name

class SRInterface(AbstractInterface):
    def __init__(self, name: str):
        super().__init__(name)
        self._data_elements = {}    

    def addDataElement(self, data_element: DataElement):
        if (data_element.name not in self._data_elements):
            if (data_element.position == 0):
                data_element.position = len(self._data_elements) + 1
            self._data_elements[data_element.name] = data_element

    def getDataElements(self)-> List[DataElement]:
        return sorted(self._data_elements.values(), key=lambda d: d.position)

class CSInterface(AbstractInterface):
    def __init__(self, name: str):
        super().__init__(name)
        self._operations = {}

    def addOperation(self, operation: Operation):
        if (operation.name not in self._operations):
            self._operations[operation.name] = operation

    def getOperations(self) -> List[Operation]:
        return sorted(self._operations.values(), key=lambda o: o.name)

class RelatedSwc:
    def __init__(self, name: str, port: str):
        self.name = name
        self.port = port
    
class Port:
    def __init__(self, name: str):
        self._name = name
        self.stereo_type = ""
        self.type = ""
        self.direction = ""
        self._senders = {}
        self._receivers = {}
        self._clients = {}
        self._servers = {}

    @property
    def name(self)-> str:
        return self._name

    def addSender(self, sender: RelatedSwc):
        if sender.name not in self._senders:
            self._senders[sender.name] = sender

    def getSenders(self) -> List[RelatedSwc]:
        return sorted(self._senders.values(), key=lambda s: s.name)

    def addReceiver(self, receiver: RelatedSwc):
        if receiver.name not in self._receivers:
            self._receivers[receiver.name] = receiver

    def getReceviers(self) -> List[RelatedSwc]:
        return sorted(self._receivers.values(), key=lambda s: s.name)

    def addClient(self, client: RelatedSwc):
        if (client.name not in self._clients):
            self._clients[client.name] = client

    def getClients(self, client) -> List[RelatedSwc]:
        return sorted(self._clients.values(), key=lambda s: s.name)

    def addServer(self, server: RelatedSwc):
        if (server.name not in self._servers):
            self._servers[server.name] = server

    def getServers(self, client) -> List[RelatedSwc]:
        return sorted(self._servers.values(), key=lambda s: s.name)

class SwComponent:
    def __init__(self, name):
        self.name = name
        self.alias = ""
        self.layer = ""
        self.note = ""
        self.enabled = False
        self.types = {}             # type: Dict[str, str]
        self._interfaces = {}       # type: Dict[str, AbstractInterface]
        self._ports = {}            # type: Dict[str, Port]
        self._operations = {}       # type: Dict[str, Operation]
        self._related_swcs = set()

    @property
    def short_name(self) -> str:
        m = re.search(r'(\w+?)_[\w_]+', self.name)
        if (m):
            return m.group(1)
        return self.name

    def addPort(self, port: Port):
        if (port.name not in self._ports):                      # Port does not exists
            self._ports[port.name] = port                       # Add the port to port list
        else:                                                   # Port has already in the port list
            for sender in port.getSenders():
                self._ports[port.name].addSender(sender)
            for receiver in port.getReceviers():
                self._ports[port.name].addReceiver(receiver)

    def getPorts(self) -> List[Port]:
        return sorted(self._ports.values(), key = lambda p: (p.direction, p.name))

    def addOperation(self, operation: Operation):
        if operation.name not in self._operations:
            self._operations[operation.name] = operation

    def getOperations(self) -> List[Operation]:
        return sorted(self._operations.values(), key = lambda o: o.name)

    def addRelatedSwc(self, swc: str):
        self._related_swcs.add(swc)
    
    def getRelatedSwcs(self) -> Set[str]:
        return sorted(self._related_swcs)

    def addInterface(self, interface: AbstractInterface):
        if interface.name not in self._interfaces:
            self._interfaces[interface.name] = interface

    def getSenderReceiverInterfaces(self) -> List[SRInterface]:
        return filter(lambda i: isinstance(i, SRInterface), self._interfaces.values())

    def getClientServerInterfaces(self) -> List[CSInterface]:
        return filter(lambda i: isinstance(i, CSInterface), self._interfaces.values())

    def getInterfaces(self) -> List[AbstractInterface]:
        return self._interfaces.values()

class SwDocument:
    def __init__(self):
        self.sw_components = {} # type: Dict[SwComponent]

    def addSwComponent(self, component: SwComponent):
        if component.name not in self.sw_components:
            self.sw_components[component.name] = component
        else:
            for port in component.getPorts():
                self.sw_components[component.name].addPort(port)
            for operation in component.getOperations():
                self.sw_components[component.name].addOperation(operation)
            for swc in component.getRelatedSwcs():
                self.sw_components[component.name].addRelatedSwc(swc)
            for interface in component.getInterfaces():
                self.sw_components[component.name].addInterface(interface)

    def _writeSenderReceiverInterface(self, parent_tag: Element, sw_component: SwComponent):
        for interface in sw_component.getSenderReceiverInterfaces():
            interface_tag = ET.SubElement(parent_tag, "INTERFACE")
            interface_tag.set("Name", interface.name)
            for element in interface.getDataElements():
                element_tag = ET.SubElement(interface_tag, "DATA_ELEMENT")
                element_tag.set("Name", element.name)
                element_tag.set("Type", element.type)

    def _writeClientServerInterface(self, parent_tag: Element, sw_component: SwComponent):
        for interface in sw_component.getClientServerInterfaces():
            interface_tag = ET.SubElement(parent_tag, "INTERFACE")
            interface_tag.set("Name", interface.name)
            for operation in interface.getOperations():
                operation_tag = ET.SubElement(interface_tag, "Method")
                operation_tag.set("Name", operation.name)
                
                for parameter in operation.getParameters():
                    paremeter_tag = ET.SubElement(operation_tag, "Parameter")
                    paremeter_tag.set("Name", parameter.name)
                    paremeter_tag.set("Type", parameter.type)
                    paremeter_tag.set("Direction", parameter.direction)

                return_type_tag = ET.SubElement(operation_tag, 'ReturnValue')
                return_type_tag.text = operation.return_type

    def _writePorts(self, parent_tag: Element, sw_component: SwComponent):
        for port in sw_component.getPorts():
            port_tag = ET.SubElement(parent_tag, "Port")
            port_tag.set("Name", port.name)
            port_tag.set("Direction", port.direction)
            port_tag.set("PortType", port.stereo_type)
            port_tag.set("Type", port.type)
            if (port.direction == "out"):
                for receiver in port.getReceviers():
                    receiver_tag = ET.SubElement(port_tag, "RECEIVER")
                    receiver_tag.set("Name", receiver.name)
                    receiver_tag.set("Port", receiver.port)
            if (port.direction == "in"):
                for sender in port.getSenders():
                    sender_tag = ET.SubElement(port_tag, "SENDER")
                    sender_tag.set("Name", sender.name)
                    sender_tag.set("Port", sender.port)

    def _writeOperations(self, parent_tag: Element, sw_component: SwComponent):
        for operation in sw_component.getOperations():
            operation_tag = ET.SubElement(parent_tag, "Method")
            operation_tag.set("Name", operation.name)
            description_tag = ET.SubElement(operation_tag, "Description")
            description_tag.text = ""
            for argument in operation.getParameters():
                argument_tag = ET.SubElement(operation_tag, "Parameter")
                argument_tag.set("Name", argument.name)
                argument_tag.set("Type", argument.type)
                argument_tag.set("Direction", argument.direction)

            return_type_tag = ET.SubElement(operation_tag, 'ReturnValue')
            return_type_tag.text = operation.return_type

    def _writeRelatedSwcs(self, parent_tag: Element, sw_component: SwComponent):
        relateds_tag = ET.SubElement(parent_tag, "RELATED_SWCS")
        for swc_name in sw_component.getRelatedSwcs():
            related_swc = SwComponent(swc_name)
            related_tag = ET.SubElement(relateds_tag, "SWC")
            related_tag.set("Name", related_swc.short_name)

    def _writeStereoType(self, parent_tag: Element, stereotype: str):
        stereotype_tag = ET.SubElement(parent_tag, "Stereotype")
        stereotype_tag.set("Name", stereotype)

    def _writeSwComponents(self, parent_tag: Element):
        for name in sorted(self.sw_components.keys()):
            sw_component = self.sw_components[name]
            sw_component_tag = ET.SubElement(parent_tag, "AtomicComponent")
            sw_component_tag.set("Name", sw_component.short_name)
            sw_component_tag.set("Layer", "")

            self._writeStereoType(sw_component_tag, "SWC")

            self._writeSenderReceiverInterface(sw_component_tag, sw_component)
            self._writeClientServerInterface(sw_component_tag, sw_component)
            self._writePorts(sw_component_tag, sw_component)
            self._writeOperations(sw_component_tag, sw_component)
            #self._writeRelatedSwcs(sw_component_tag, sw_component)

    def writeXml(self, file_name: str):
        root_tag = ET.Element('Document')
        root_tag.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root_tag.set("xsi:noNamespaceSchemaLocation", "arch_element.xsd")

        self._writeSwComponents(root_tag)

        # create a new XML file with the results
        data = ET.tostring(root_tag, encoding="utf-8" ).decode("utf-8")
        reparsed = minidom.parseString(data)
        with open(file_name, 'w') as f_out:
            f_out.write(reparsed.toprettyxml(indent="\t"))

    def _readNote(self, parent_tag):
        note_tag = parent_tag.find('NOTES')
        if note_tag is None:
            return None
        return note_tag.text

    def _readPortDataElements(self, parent_tag, port: Port):
        for data_element_tag in parent_tag.findall('DATA_ELEMENT'):
            data_element = DataElement(data_element_tag.attrib['Name'])
            data_element.type = data_element_tag.attrib['Type']
            port.addDataElement(data_element)

    def _readSenders(self, parent_tag, port: Port):
        for sender_tag in parent_tag.findall("SENDER"):
            port.addSender(sender_tag.attrib['Name'], sender_tag.attrib['Port'])

    def _readReceivers(self, parent_tag, port: Port):
        for receiver_tag in parent_tag.findall('RECEIVER'):
            port.addReceiver(receiver_tag.attrib['Name'], receiver_tag.attrib['Port'])

    def _readDirection(self, direction : str):
        if (direction == 'in'):
            return "in"
        elif (direction == 'out'):
            return "out"
        elif (direction == "inout"):
            return "inout"
        else:
            raise Exception("Invalid parameter direction <%s>" % (direction))

    def _readPorts(self, parent_tag, swc: SwComponent):
        for port_tag in parent_tag.findall('Port'):
            name = port_tag.attrib['Name']
            port = swc.createPort(name)
            port.stereo_type = port_tag.attrib['PortType']
            port.type = port_tag.attrib['Type']
            port.direction = self._readDirection(port_tag.attrib['Direction'])
            if (port.direction == "in"):
                self._readSenders(port_tag, port)
            elif (port.direction == "out"):
                self._readReceivers(port_tag, port)

            self._readPortDataElements(port_tag, port)

    def _readOperationParameters(self, parent_tag, operation: Operation):
        for param_tag in parent_tag.findall('PARAMETER'):
            param = Parameter()
            param.name = param_tag.attrib['Name']
            param.type = param_tag.attrib['Type']
            param.direction = self._readDirection(param_tag.attrib['Direction'])
            operation.addParameter(param)

    def _readOperations(self, parent_tag, swc: SwComponent):
        for operation_tag in parent_tag.findall('OPERATION'):
            name = operation_tag.attrib['Name']
            operation = swc.createOperation(name)
            operation.return_type = operation_tag.attrib['ReturnType']
            note = self._readNote(operation_tag)
            if (note == None):
                operation.note = ""
            else:
                operation.note = note
            self._readOperationParameters(operation_tag, operation)

    def _readSwComponents(self, root_tag):
        for swc_tag in root_tag.findall('SWC'):
            swc_name = swc_tag.attrib['Name']
            swc = SwComponent(swc_name)
            if ('Alias' in swc_tag.attrib):
                swc.alias = swc_tag.attrib['Alias']
            if ('Layer' in swc_tag.attrib):
                swc.layer = swc_tag.attrib['Layer']
            if ('Enabled' in swc_tag.attrib):
                if (swc_tag.attrib['Enabled'] == "true"):
                    swc.enabled = True
                else:
                    swc.enabled = False
            note = self._readNote(swc_tag)
            if (note != None):
                swc.note = note 
            self._readOperations(swc_tag, swc)
            self._readPorts(swc_tag, swc)

    def readXml(self, file_name: str):
        tree = ET.parse(file_name)
        root_tag = tree.getroot()
        self._readSwComponents(root_tag)