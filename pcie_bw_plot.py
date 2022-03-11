import math
import matplotlib.pyplot as plt

from pcie_constant import *


# Return the PCIe write bandwidth
def pcie_write(bw, mps, size):
    mwr_hdr = 24
    raw_bytes = math.ceil(size / mps) * mwr_hdr + size
    return (size / raw_bytes) * bw 

# Return the PCIe read bandwith
def pcie_read(bw, mps, size):
    cpl_hdr = 20
    raw_bytes = math.ceil(size / mps) * cpl_hdr + size
    return (size / raw_bytes) * bw 

# When read and write happens together, 
# read will occupy a little bit of the tx bandwidth
def pcie_wr(bw, mps, mrrs, size):
    mrd_hdr = 24
    mwr_hdr = 24
    raw_bytes = math.ceil(size / mps) * mwr_hdr + size + math.ceil(size / mrrs) * mrd_hdr
    return (size / raw_bytes) * bw

if __name__ == "__main__":
    # Get the bandwidth of this pcie configuration
    bw_raw, bw_phy, bw_ddl, mps, mrrs = pcie_conf()

    size_list = []
    pcie_write_bw_list = []
    pcie_read_bw_list = []
    pcie_wr_bw_list = []
    for size in range(64, 1500+1):
        pcie_write_bw = pcie_write(bw_ddl, mps, size)
        pcie_read_bw =  pcie_read(bw_ddl, mps, size)
        pcie_wr_bw = pcie_wr(bw_ddl, mps, mrrs, size)

        size_list.append(size)
        pcie_write_bw_list.append(pcie_write_bw / (10 ** 9))
        pcie_read_bw_list.append(pcie_read_bw / (10 ** 9))
        pcie_wr_bw_list.append(pcie_wr_bw / (10 ** 9))
    
    plt.axhline(y=bw_raw / (10 ** 9), label="PCIe Raw Bandwidth", color='gray', linestyle=":")
    plt.axhline(y=bw_phy / (10 ** 9), label="PCIe Effective Bandwidth in Physical Layer", color='gray', linestyle="--")
    plt.axhline(y=bw_ddl / (10 ** 9), label="PCIe Effective Bandwidth in Data Link Layer", color='gray', linestyle="-.")

    plt.plot(size_list, pcie_write_bw_list, label="PCIe Write Bandwidth", color='blue') 
    plt.plot(size_list, pcie_read_bw_list, label="PCIe Read Bandwidth", color='red') 
    plt.plot(size_list, pcie_wr_bw_list, label="PCIe Write Bandwidth with Simultaneous Read", color='brown') 
    plt.xlabel("Transfer Size (Bytes)")
    plt.ylabel("Bandwidth (Gb/s)")
    plt.legend()
    plt.savefig("figures/pcie-bw.jpg")