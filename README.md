This package is not yet in PyPI. For now you can clone the respository and
install it directly with `pip`.

The only facility at present are convenince objects for building
`fontforge.askMulti()` specifications. Here is a brief example:

```
import fontforge
from fontforge_helper.multidialog import *

q = MultiChoice("A choice", tag=1, multiple=True, checks=True)

q.add_answer(MultiAnswer("foo"))
q.add_answer(MultiAnswer("bar", default=True))

q2 = MultiString("A string", tag=2, default='bar')
q3 = MultiOpen("An Open", tag=3, default='/tmp/bar', fltr='*.txt')

c = MultiCategory("cat a")
c.add_question(q)
c.add_question(q2)

c2 = MultiCategory("cat b")
c2.add_question(q3)

d = MultiDialog()
d.add_category(c)
d.add_category(c2)

fontforge.askMulti("title", d)

```

All question objects (`MultiString`, `MultiChoice`, `MultiSave`, and
`MultiOpen`) have `label` (first parameter) , `tag`, and `align` construtor
parameters. each of these is also a property on the object. Every question
object besides `MultiChoice` has a `default` parameter/property and the path
objects also have a `fltr` parameter/property.

`MultiChoice` has boolean `multiple` and `checks` parameters/properties and an
`add_answer` method for adding `MultiAnswer` objects. Those have `name`, `tag`
and `default` parameters/properties.

A `MultiCategory` object has a `label` parameter/property and an `add_question`
method for adding question objects.

A `MultiDialog` object just has an `add_category` method for adding `MultiCategory`
objects.

There are also some getters and setters for the lists, check the code. They
generally do deep copies.

All of these parameters and properties correspond to the lists and dictionaries
described in the added askMulti TechRef document.
