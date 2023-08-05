This is a package that allows you to easily diff a single line. The following are some examples (note that in this example spaces are used instead of bullets due :

>>> diff("This is totally just my opinion.", "This is simply my opinion.")
This is totally just my opinion.
This is simp‐ly‐‐‐‐‐ my opinion.
        ^^^^^  ^^^^^            

>>> diff("I called but no one answered.", "I tried calling, but no one answered.")
I‐‐‐‐‐‐ called‐‐ but no one answered.
I tried calling, but no one answered.
 ^^^^^^     ^^^^                     