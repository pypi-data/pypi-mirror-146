# Ultimate Parser

---

### How to use the module?

For example, I will use this page:
https://swanchick.github.io/Swanchick-s-Software/

---

Initialize Parse class:
```py
parse = Parse("https://swanchick.github.io/Swanchick-s-Software/")
```

Get title from page:
```py
print(parse.get_title())
```

Update parse:
```py
parse.update()
```

```py
parse.update("URL")
```

Get all elements by name:

```py
for el in parse.find_by_element_name("img"):
    print(el.options)
```

Find html elemnt by class:

```py
for el in parse.find_by_class("description"):
    print(el.name)
    print(el.options)
```

Find html elemnt by id
*ps: This page don't have element, which have id option inside.*
```py
for el in parse.find_by_id("sample-id"):
    print(el.name)
    print(el.options)
```

Class Element has fields:
- name (str)
- options (dict)
- content (any)