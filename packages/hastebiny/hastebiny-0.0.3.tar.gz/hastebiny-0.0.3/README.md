# hastebiny
An unofficial hastebin module.

`pip install hastebiny`

This is a simpe module that allows you to create and recieve hastebins. Using the send function, you can send data (text) to hastebins server and store it there, the function will return a key to access this data.
The get function will return the data (text) attributed to a key.

```py
# Example code
from hastbiny import hb

key = hb.send("My hastebin content :)")
print(key)
print(hb.get(key))
```