from armodel import AUTOSAR, ARPackage, SwComponentType, AtomicSwComponentType, CompositionSwComponentType, SenderReceiverInterface, ClientServerInterface
from armodel import TimingEvent, OperationInvokedEvent, SwComponentPrototype, ProvidedPortPrototypeInstanceRef, RequiredPortPrototypeInstanceRef
from armodel import VariableAccess, ApplicationDataType, ImplementationDataType, ClientServerOperation, PPortPrototype, RPortPrototype
from armodel import ARXMLParser

from model.sw_model import SwComponent, SwDocument, Operation, Parameter, DataElement, Port, RelatedSwc, SRInterface, CSInterface

class ARXML2Doc:
    def __init__(self):
        self.document = None    #type: AUTOSAR

    def _process_variable_access(self, suffix: str, variable_access: VariableAccess):
        #port = self.document.find(variable_access.accessed_variable_ref.autosar_variable_in_impl_datatype.port_prototype_ref.value)  # type: RPortPrototype
        data_element = self.document.find(variable_access.accessed_variable_ref.autosar_variable_in_impl_datatype.target_data_prototype_ref.value)
        data_type = self.document.find(data_element.type_tref.value)
        if (isinstance(data_type, ApplicationDataType)):
            data_type = self.document.convertToImplementationDataType(data_type.full_name)

        self._process_data_type(data_type)


    def _process_data_type(self, data_type: ImplementationDataType):
        if (data_type.category == ImplementationDataType.CATEGORY_TYPE_REFERENCE):
            pass
        #    referred_type = self.document.getDataType(data_type)

# def process_server_call(document: AUTOSAR, server_call_point: ServerCallPoint):
#    port = document.find(server_call_point.operation_iref.conext_r_port_ref.value)                  # type: RPortPrototype
#    operation = document.find(server_call_point.operation_iref.target_required_operation_ref.value) # type: ClientServerOperation


#    for argument in operation.getArgumentDataPrototypes():
#        data_type = document.find(argument.type_tref.value)
#        if (isinstance(data_type, ApplicationDataType)):
#            data_type = document.convertToImplementationDataType(data_type.full_name)
#
#        process_data_type(document, data_type)

    def _process_operation_invoked_event(self, swc: SwComponent, event: OperationInvokedEvent):
        target_operation = self.document.find(event.operation_iref.target_provided_operation_ref.value)  # type: ClientServerOperation
        entity = self.document.find(event.start_on_event_ref.value)

        operation = Operation(entity.symbol)

        if (len(target_operation.getPossbileErrorRefs()) > 0):
            operation.return_type = "Std_ReturnType"
        else:
            operation.return_type = "void"

        for argument in target_operation.getArgumentDataPrototypes():
            data_type = self.document.find(argument.type_tref.value)
            if (isinstance(data_type, ApplicationDataType)):
                data_type = self.document.convertToImplementationDataType(data_type.full_name)

            parameter = Parameter()
            parameter.name = argument.short_name
            parameter.direction = argument.direction.lower()
            parameter.type = data_type.short_name
            operation.addParameter(parameter)

        swc.addOperation(operation)


    def _process_timing_event(self, swc: SwComponent, event: TimingEvent):
        entity = self.document.find(event.start_on_event_ref.value) # type: RunnableEntity

        operation = Operation(entity.symbol)
        operation.return_type = "void"

        swc.addOperation(operation)

    def _process_behavior(self, swc: SwComponent, sw_component: AtomicSwComponentType):
        for event in sw_component.internal_behavior.getOperationInvokedEvents():    # type: OperationInvokedEvent
            self._process_operation_invoked_event(swc, event)
        for event in sw_component.internal_behavior.getTimingEvents():
            self._process_timing_event(swc, event)

    def _get_port_interface_name(self, type_name: str):
        port_interface = self.document.find(type_name)
        return port_interface.short_name

    def _process_sw_component(self, sw_doc: SwDocument, sw_component: SwComponentType):
        swc = SwComponent(sw_component.short_name)

        for pport_prototype in sw_component.getPPortPrototypes():
            port = Port(pport_prototype.short_name)
            if (pport_prototype.provided_interface_tref.dest == "SENDER-RECEIVER-INTERFACE"):
                port.stereo_type = "Sender"
            elif (pport_prototype.provided_interface_tref.dest == "CLIENT-SERVER-INTERFACE"):
                port.stereo_type = "Server"
            else:
                raise ValueError("Invalid provided interface <%s>" % port.short_name)    
            port.direction = "out"
            port.type = self._get_port_interface_name(pport_prototype.provided_interface_tref.value)
            swc.addPort(port)

        for rport_prototype in sw_component.getRPortPrototypes():
            port = Port(pport_prototype.short_name)
            if (rport_prototype.required_interface_tref.dest == "SENDER-RECEIVER-INTERFACE"):
                port.stereo_type = "Receiver"
            elif (rport_prototype.required_interface_tref.dest == "CLIENT-SERVER-INTERFACE"):
                port.stereo_type = "Client"
            else:
                raise ValueError("Invalid provided interface <%s>" % port.short_name)    
            port.direction = "in"
            port.type = self._get_port_interface_name(pport_prototype.provided_interface_tref.value)
            swc.addPort(port)

        if (isinstance(sw_component, AtomicSwComponentType)):
            self._process_behavior(swc, sw_component)
        sw_doc.addSwComponent(swc)

    def _process_sender_receiver_interface(self, swc: SwComponent, port: Port, interface_name: str):
        port_interface = self.document.find(interface_name)  # type: SenderReceiverInterface
        port.type = port_interface.short_name

        sr_interface = SRInterface(port_interface.short_name)

        for data_element in port_interface.getDataElements():
            data_type = self.document.find(data_element.type_tref.value)
            if (isinstance(data_type, ApplicationDataType)):
                data_type = self.document.convertToImplementationDataType(data_type.full_name)

            element = DataElement(data_element.short_name)
            element.type = data_type.short_name
            sr_interface.addDataElement(element)

        swc.addInterface(sr_interface)

    def _process_client_server_interface(self, swc: SwComponent, port: Port, interface_name: str):
        """ read the client server interface from ARXML """

        port_interface = self.document.find(interface_name)  # type: ClientServerInterface
        port.type = port_interface.short_name

        cs_interface = CSInterface(port_interface.short_name)

        for operation in port_interface.getOperations():
            op = Operation(operation.short_name)
            if len(operation.getPossbileErrorRefs()) == 0:
                op.return_type = "void"
            else:
                op.return_type = "Std_ReturnType"
            for parameter in operation.getArgumentDataPrototypes():
                param = Parameter()
                param.name = parameter.short_name
                data_type = self.document.find(parameter.type_tref.value)
                if (isinstance(data_type, ApplicationDataType)):
                    data_type = self.document.convertToImplementationDataType(
                        data_type.full_name)
                param.type = data_type.short_name
                param.direction = parameter.direction
                op.addParameter(param)
            cs_interface.addOperation(op)

        swc.addInterface(cs_interface)

    def _process_port(self, swc_src: SwComponent, swc_dst: SwComponent, port_src: PPortPrototype, port_dst: RPortPrototype):
        p_port = Port(port_src.short_name)
        p_port.direction = "out"
        p_port.addReceiver(RelatedSwc(swc_dst.short_name, port_dst.short_name))

        if (port_src.provided_interface_tref.dest == "SENDER-RECEIVER-INTERFACE"):
            p_port.stereo_type = "Sender"
            self._process_sender_receiver_interface(swc_src, p_port, port_src.provided_interface_tref.value)
        elif (port_src.provided_interface_tref.dest == "CLIENT-SERVER-INTERFACE"):
            p_port.stereo_type = "Server"
            self._process_client_server_interface(swc_src, p_port, port_src.provided_interface_tref.value)
        else:
            raise ValueError("Invalid provided interface <%s>" %
                            port_src.short_name)

        swc_src.addPort(p_port)

        r_port = Port(port_dst.short_name)
        r_port.direction = "in"
        r_port.addSender(RelatedSwc(swc_src.short_name, port_src.short_name))

        if (port_dst.required_interface_tref.dest == "SENDER-RECEIVER-INTERFACE"):
            r_port.stereo_type = "Receiver"
            self._process_sender_receiver_interface(swc_dst, r_port, port_dst.required_interface_tref.value)
        elif (port_dst.required_interface_tref.dest == "CLIENT-SERVER-INTERFACE"):
            r_port.stereo_type = "Client"
            self._process_client_server_interface(swc_dst, r_port, port_dst.required_interface_tref.value)
        else:
            raise ValueError("Invalid provided interface <%s>" % port_src.short_name)

        swc_dst.addPort(r_port)

        swc_src.addRelatedSwc(swc_dst.name)
        swc_dst.addRelatedSwc(swc_src.name)

    def _process_assembly_connect(self, sw_doc: SwDocument, provider: ProvidedPortPrototypeInstanceRef, requester: RequiredPortPrototypeInstanceRef):
        prototype_src = self.document.find(provider.context_component_ref.value)     # type: SwComponentPrototype
        p_port = self.document.find(provider.target_p_port_ref.value)                # type: PPortPrototype
        sw_component_src = self.document.find(prototype_src.type_tref.value)

        prototype_dst = self.document.find(requester.context_component_ref.value)    # type: SwComponentPrototype
        r_port = self.document.find(requester.target_r_port_ref.value)
        sw_component_dst = self.document.find(prototype_dst.type_tref.value)

        swc_src = SwComponent(sw_component_src.short_name)
        swc_dst = SwComponent(sw_component_dst.short_name)

        self._process_port(swc_src, swc_dst, p_port, r_port)

        sw_doc.addSwComponent(swc_src)
        sw_doc.addSwComponent(swc_dst)

    def _process_composition_sw_component(self, sw_doc: SwDocument, composition_sw_component: CompositionSwComponentType):
        for prototype in composition_sw_component.getSwComponentPrototypes():
            sw_component = self.document.find(prototype.type_tref.value)
            self._process_sw_component(sw_doc, sw_component)
        for connector in composition_sw_component.getAssemblySwConnectors():
            self._process_assembly_connect(sw_doc, connector.provider_iref, connector.requester_iref)

    def _process_ar_package(self, sw_doc: SwDocument, ar_package: ARPackage):
        for sw_component in ar_package.getAtomicSwComponentTypes():
            self._process_sw_component(sw_doc, sw_component)    
        for child_pkg in ar_package.getARPackages():
            self._process_ar_package(sw_doc, child_pkg)

    def covert_arxml_files_to_sw_doc(self, arxml_files) -> SwDocument:
        self.document = AUTOSAR.getInstance()

        sw_doc = SwDocument()
        parser = ARXMLParser()

        for arxml_file in arxml_files:
            parser.load(arxml_file, self.document)

        # sw_doc.readXml(xml_file)

        for child_pkg in self.document.getARPackages():
            self._process_ar_package(sw_doc, child_pkg)

        return sw_doc


    def convert_arxml_2_swc_xml(self, arxml_files, xml_file: str):
        sw_doc = self.covert_arxml_files_to_sw_doc(arxml_files)
        sw_doc.writeXml(xml_file)