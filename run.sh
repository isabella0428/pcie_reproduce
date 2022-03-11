if [ ! -d "figures" ]; then
    mkdir figures
fi

python pcie_bw_plot.py
python nic_bw_plot.py