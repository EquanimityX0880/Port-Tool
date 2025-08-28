import array
import miniupnpc
import time

def read_file(file = "ports.txt"):

    with open(file, 'r') as f:
        lines = f.readlines()
    
    lines = [line.strip() for line in lines]
    return lines

def open_ports(ports, description="UPnP Port Forwarding"):
    # Create the UPnP object
    upnp = miniupnpc.UPnP()
    upnp.discoverdelay = 200
    upnp.discover()  # Discover devices on the network
    upnp.selectigd()  # Select the Internet Gateway Device (router)
    

    print(f"Local IP Address: {upnp.lanaddr}")
    print(f"Public IP Address: 167.224.155.162")

    for port in ports:
        external_port = port['external_port']
        internal_port = port.get('internal_port', external_port)  # Same as external unless specified
        protocol = port['protocol'].upper()

        try:
            upnp.addportmapping(external_port,protocol,upnp.lanaddr,internal_port,description,'')
            print(f"Opened {protocol} port {external_port} -> {internal_port}")

        except Exception as e:
            print(f"Failed to open {protocol} port {external_port}: {e}")

    print(f"Closing this prompt in 5 seconds...")
    time.sleep(5)

if __name__ == "__main__":
    ports_to_open = []
    ports = read_file()
    # print(ports)

    for i in ports:
        ports_to_open.append({'external_port': int(i), 'protocol': 'TCP'})
        ports_to_open.append({'external_port': int(i), 'protocol': 'UDP'})

    open_ports(ports_to_open)
