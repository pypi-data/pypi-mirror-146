## Crack

Crack tools all here!

Currently support custom aes, base58, base64, secrets, seal box, unsigned shift and font decode, other will be coming soon.

Thanks for use.


### How to use
#### Base58
```python
import crack


crack.b58encode("leesoar.com")
# Return: Tt1fb89EdWohEDa

crack.b58decode("Tt1fb89EdWohEDa")
# Return: leesoar.com
```


#### Base64
```python
import crack


crack.b64encode(b"leesoar.com", b64_map="9240gsB6PftGXnlQTw_pdvz7EekDmuAWCVZ5UF-MSK1IHOchoaxqYyj8Jb3LrNiR")
# Return: DBvFmjNVmZb5DjY=

crack.b64decode("DBvFmjNVmZb5DjY=", b64_map="9240gsB6PftGXnlQTw_pdvz7EekDmuAWCVZ5UF-MSK1IHOchoaxqYyj8Jb3LrNiR")
# Return: b'leesoar.com'
```


#### Decimal to other
```python
import crack


# default base is 58
crack.dec_to_other(9527)
# Return: [2, 48, 15]
```


#### Font Decode
> Thanks fonttools.

If a site font was displayed wrong, it can be corrected like this: 
```python
from crack import Font

font = Font("font_file.ttf")
font.mapping([1, 3, 2, 4, 0, 5, 7, 8, 6, 9], start=2)
font.load(Font("https://nskol.com/font/default.ttf"))
font.decode("\ue627\ueb1c\uefc6")   # This is the correct result.
```


#### Array's partition
```python
import crack


[print(x, end=", ") for x in crack.partition("gmapi.cn", size=3)]
# Print: gma, pi., cn, 


[print(x) for x in crack.partition(["g", "m", "a", "p", "i", ".", "c", "n"], size=3)]
# Print: ['g', 'm', 'a'], ['p', 'i', '.'], ['c', 'n'], 
```

### Unsigned shift
```python
import crack


crack.unsigned_right_shift(-2048, 1)
# Output: 2147482624
# It likes JavaScript ">>>"

...

```


### AES
* **If you use 'from crack import Aes', it will automatically fix the bug of importing crypto error.**
```python
from crack import Aes


aes = Aes(key="xxxxxxxxx", iv="xxxxxxxxx")
aes.encrypt_hex(b"xxxxxxxxxxx")
aes.encrypt_byte(b"xxxxxxxxxxx")
...

```



### Secrets
```python
import crack


crack.token_hex(16)
# Output: 984a0877240ec62afaf6bbab175ab985  [Random]

...

```