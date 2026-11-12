Changes
=======


0.3.12
------

Some more experimental features were added, mainly regarding the support of mobile agents.
The work was mainly contributed by Els Kuipers during her `MSc thesis <https://studenttheses.uu.nl/items/14c93095-3517-422f-bd0e-4ab1a42e9168>`_.

The versions 0.3.7 to 0.3.11 were unpublished development releases.


0.3.6
-----

Setting the random seed changed.
`seed` as argument for individual operations was removed.
Using `pcr.setrandomseed` is no longer necessary.

Use an integer to fix the seed at `campo.Campo()` for reproducible results.
Be default, arbitrary random values will be returned.
