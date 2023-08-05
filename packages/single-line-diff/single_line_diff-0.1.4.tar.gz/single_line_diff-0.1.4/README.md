This is a package that allows you to easily diff a single line. The following are some examples (note that in this example underscores are used instead of bullets due to not rendering properly on Pypi):

>>> diff("This is totally just my opinion.", "This is simply my opinion.")
This is totally just my opinion.
This is simp_ly_____ my opinion.
        ^^^^^  ^^^^^            

>>> diff("I called but no one answered.", "I tried calling, but no one answered.")
I______ called__ but no one answered.
I tried calling, but no one answered.
 ^^^^^^     ^^^^                     