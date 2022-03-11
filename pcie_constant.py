import json

pcie_transfer_rate = {
    "gen3": 8 * (10 ** 9)
}

pcie_encoding_efficiency = {
    "128b/130b": 128 / 130
}

# Return the effective bandwidth at the Phy and DDL layer
def pcie_conf():
    with open("pcie.json") as f:
        data = json.load(f)
    bw_raw = pcie_transfer_rate[data["version"]] * float(data["num_lanes"])
    bw_phy = bw_raw * pcie_encoding_efficiency[data["encoding"]]
    bw_ddl = bw_phy * (1 - data["dll_overhead"])

    return bw_raw, bw_phy, bw_ddl, data["MPS"], data["MRRS"]
