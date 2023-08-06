# Witaker Clipboard Server
## A utility for copy and paste in the browser without requiring focus

For security reasons, web browsers don't allow text to be copied to the system
clipboard when the browser window is not focused. There are use cases where 
you might want to copy text quickly by hovering or swiping your mouse over a
background window, for instance when testing a web application. This allows a
user to "pick up" a test value by hovering their mouse pointer, and speeds up
testing.

Witaker Clipboard Server is a utility which provides a local web server for
JavaScript applications to interact with, so it can copy text to your computer's
clipboard while in a background state. The Clipboard Server will start with an
authentication key, which your JavaScript application will need to reference
before calling the server.


## Features

Witaker Clipboard Server is a Python 3 program, with a command-line application, and a GUI, written with [Kivy](https://kivy.org).

- witaker-clipboard-server
- witaker-clipboard-server-gui

At its core is a microservice, written with [Flask](https://flask.palletsprojects.com/en/2.0.x/), which interacts with the system clipboard using [xerox](https://github.com/adityarathod/xerox).


## Installation

You can install Witaker Clipboard Server with pip:



```sh
pip install witaker-clipboard-server
```


## License

Copyright © 2022 Cathal Mc Ginley

Licensed under the **Apache License, Version 2.0** (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the [License](LICENSE) at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

