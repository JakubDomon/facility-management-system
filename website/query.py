class QueryMachines:

    def __init__(self,) -> None:
        pass

    def get_names(self, Machines):
        
        machines = Machines.query.all()

        names = []

        for machines in machines:
            names.append(str(machines.name))
        
        return names


    def get_endpoints(self, Machines):
        
        machines = Machines.query.all()

        endpoints = []

        for machines in machines:
            endpoints.append(str(machines.name))
        
        return endpoints


    def get_nodes(self, Machines):
        
        machines = Machines.query.all()

        nodesSensors = []
        nodesData = []
        nodesProduction = []

        for machines in machines:
            nodesSensors.append(str(machines.opcua.nodesSensors))
            nodesData.append(str(machines.opcua.nodesData))
            nodesProduction.append(str(machines.opcua.nodesProduction))
        
        return nodesProduction, nodesData, nodesSensors


    def get_all(self, Machines):

        machines = Machines.query.all()

        names = []
        endpoints = []

        for machines in machines:
            names.append(str(machines.name))
            endpoints.append(str(machines.opcua.endpoint))

        return names, endpoints