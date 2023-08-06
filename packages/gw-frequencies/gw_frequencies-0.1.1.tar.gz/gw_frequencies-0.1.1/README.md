# gw_frequencies
A convenience package to make reduced frequency arrays for the representation of gravitational waveforms.

It makes available the following functions; here they are documented 
very shortly, see their docstrings (`help(func_name)`  in an interactive console)
for more details.

- `seglen_from_freq`, which computes the duration T(f), in seconds, 
    of a gravitational wave signal starting at a given frequency, in Hertz.
- `high_frequency_grid`, a uniform grid in frequency
- `low_frequency_grid`, a non-uniform grid in frequency satisfying dN/df = 1/T(f) at each frequency 
- `mixed_frequency_grid`, a grid with the low-frequency specification below some pivot 
    and the high-frequency specification above it.

The main idea here is the `low_frequency_grid`, which is a slightly different implementation of the 
concepts outlined by [Vinciguerra et al, 2017](http://arxiv.org/abs/1703.02062).

To install this package, do:
```bash
pip install gw-frequencies
```

To import the required functions, do 
```python
from gw_frequencies.multibanding import <func_name>
```
where `<func name>` is the name of the function you want.

