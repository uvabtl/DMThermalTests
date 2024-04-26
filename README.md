# DMThermalTests
Thermal QA/QC measurement for BTL DetectorModules

- To start logging temperatures
```
python3 ./read_PT1000.py --dev /dev/ttyACM0 --log run0001.log
```

- To create a self-updating plot to monitor the temperatures:
```
python3 ./plot_PT1000.py run0001.log
```
