Changes
=======


0.3.6
-----

Setting the random seed changed.
`seed` as argument for individual operations was removed.
Using `pcr.setrandomseed` is no longer necessary.

Use an integer to fix the seed at `campo.Campo()` for reproducible results.
Be default, arbitrary random values will be returned.
