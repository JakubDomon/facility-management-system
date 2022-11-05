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

        nodes = []

        for machines in machines:
            nodes.append(str(machines.name))
        
        return nodes


    def get_all(self, Machines):

        machines = Machines.query.all()

        names = []
        endpoints = []
        nodesID = []

        for machines in machines:
            names.append(str(machines.name))
            endpoints.append(str(machines.opcua.endpoint))
            nodesID.append(str(machines.opcua.nodes))

        return names, endpoints, nodesID