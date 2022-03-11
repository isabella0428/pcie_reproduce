import math
import matplotlib.pyplot as plt
from sqlalchemy import over

from pcie_constant import *

# The bandwidth when NIC tx packet
def nic_tx(bw, mps, mrrs, size, interrupt=1):
    # 1) Host upates the Tx queue tail pointer (PCIe write)
    # 2) Device DMAs decriptor                 (PCIe read)
    # 3) Device DMAs packet content            (PCIe read)
    # 4) Device generates interrupt            (PCIe write)
    # 5) Host reads Tx queue head pointer      (PCIe read)
    mwr_hdr = mrd_hdr = 24
    cpl_hdr = 20

    pointer_size = 4
    descriptor_size = 16
    interrupt_size = 4

    raw_bytes = math.ceil(pointer_size / mps) * mwr_hdr + pointer_size
    raw_bytes += math.ceil(interrupt * descriptor_size / mps) * cpl_hdr + interrupt * descriptor_size
    raw_bytes += math.ceil(interrupt * size / mps) * cpl_hdr + interrupt * size
    raw_bytes += math.ceil(interrupt * interrupt_size / mps) * mwr_hdr + interrupt_size
    raw_bytes += math.ceil(pointer_size / mrrs) * mrd_hdr

    return (interrupt * size / raw_bytes) * bw

# The bandwidth when NIC rx packet 
def nic_rx(bw, mps, mrrs, size, interrupt=1):
    # 1) Host updates Rx Queue Tail Pointer  (PCIe write)       
    # 2) Device DMA descriptors from host    (PCIe read)
    # 3) Device DMAs packet to host          (PCIe write)
    # 4) Device writes back RX descriptor    (PCIe write)
    # 5) Device generate interrupts          (PCIe write)
    # 6) Host reads RX queue head pointer    (PCIe read)
    mwr_hdr = mrd_hdr = 24
    cpl_hdr = 20

    pointer_size = 4
    descriptor_size = 16
    interrupt_size = 4

    raw_bytes = math.ceil(interrupt * descriptor_size / mrrs) * mrd_hdr
    raw_bytes += math.ceil(interrupt * size / mps) * mwr_hdr + interrupt * size
    raw_bytes += math.ceil(interrupt * descriptor_size / mps) * mwr_hdr + interrupt * descriptor_size
    raw_bytes += math.ceil(interrupt_size / mps) * mwr_hdr + interrupt_size
    raw_bytes += math.ceil(pointer_size / mps) * cpl_hdr + pointer_size

    return (interrupt * size) / raw_bytes * bw

if __name__ == "__main__":
    # Get the bandwidth of this pcie configuration
    bw_raw, bw_phy, bw_ddl, mps, mrrs = pcie_conf()

    size_list = []
    nic_tx_bw_list_1 = []
    nic_tx_bw_list_10 = []

    nic_rx_bw_list_1 = []
    nic_rx_bw_list_10 = []

    for size in range(64, 1500+1):
        size_list.append(size)
        nic_tx_bw_list_1.append(nic_tx(bw_ddl, mps, mrrs, size, interrupt=1) / (10 ** 9))
        nic_tx_bw_list_10.append(nic_tx(bw_ddl, mps, mrrs, size, interrupt=10) / (10 ** 9))

        nic_rx_bw_list_1.append(nic_rx(bw_ddl, mps, mrrs, size, interrupt=1) / (10 ** 9))
        nic_rx_bw_list_10.append(nic_rx(bw_ddl, mps, mrrs, size, interrupt=10) / (10 ** 9))


    plt.plot(size_list, nic_tx_bw_list_1, label="NIC TX Bandwidth (interrupt=1)", color='blue') 
    plt.plot(size_list, nic_tx_bw_list_10, label="NIC TX Bandwidth (interrupt=10)", color='red') 

    plt.plot(size_list, nic_rx_bw_list_1, label="NIC RX Bandwidth (interrupt=1)", color='purple') 
    plt.plot(size_list, nic_rx_bw_list_10, label="NIC RX Bandwidth (interrupt=10)", color='cyan') 

    plt.xlabel("Packet Size (Bytes)")
    plt.ylabel("Bandwidth (Gb/s)")
    plt.legend()
    plt.savefig("figures/nic-bw.jpg")