# Easy LUT Init String manipulation

You only need two things:

1. A pin mapping given by rapidwright.
2. A 64 bit initstring in hex format like `0x0123456789ABCDEF`

Then by using the following you can obtain the init string found in the bitstream
```python
from lutstrings import lut
bitstream_init_string = lut.fullConversion(pin_mapping, init_string)
```


The pin mapping can be obtained using rapidwright from a LUT cell with

```python
pin_mapping = cell_lut.getPinMappingsL2P()
```

This currently only works for 6 input luts with 64 bit init strings