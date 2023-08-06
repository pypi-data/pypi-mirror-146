![Python version](https://img.shields.io/badge/Python->%3D3.9-blue?style=flat&logo=python&logoColor=yellow&link=https://www.python.org/downloads/)

# Bleep-it
Text filtering tool

# :clipboard:  Table Of Content
[Installation](#installation)  
[Quickstart](#quickstart)  
[Documentation](#documentation)  
[Bleep-it Tools](#bleep-it-tools)  
[License](LICENSE)  

# Installation
```cmd
pip install bleep-it
# OR
pip install https://github.com/Marseel-E/bleep-it
```

# Quickstart
```py
import asyncio
import bleep


async def main():
  while True:
    text = input("text: ")

    filtered_text = await bleep.filter(text=text, strickness=2)

    print("filtered_text:", filtered_text)


if __name__ == '__main__':
  asyncio.run(main())
```

# Documentation
### `async` filter
```py
await filter(text, strickness=2, action=Censor())
```
This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Filters the text given and returns the filtered test.

#### Parameters
- text ( [str](https://docs.python.org/3/library/stdtypes.html#str) ) - The text to be filtered.  
- strickness ( [int](https://docs.python.org/3/library/functions.html#int) ) - The level of strickness of the filtering.  
- action ( [Censor](#censor) | [Remove](#remove) ) - The action to take when filtering a word.  
 
#### Returns
The filtered text.

#### Return type
[str](https://docs.python.org/3/library/stdtypes.html#str)  

<hr />  

### `class` Censor
Sensors the filtered word.

#### Methods
- `async` generate 

#### `await generate(word)`
This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Generates the censorship to replace the word with.

##### Parameters
- word ( [str](https://docs.python.org/3/library/stdtypes.html#str) ) - The word to be censored.

##### Returns
The censored replacement for the word.

##### Return type
[str](https://docs.python.org/3/library/stdtypes.html#str)  

<hr />

### `class` Remove
Removes the filtered word from the text.


# Bleep-it Tools
[Bleep-it Tools](https://github.com/Marseel-E/bleep-it-tools) is an extension for Bleep-it that allows you to
- [x] Create custom words.  
- [ ] ~~Generate other languages.~~ `soon`

### :scroll: [License](LICENSE)
