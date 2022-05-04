<div id="top"></div>

<br />
<div align="center">
    <img src="https://selflanguage.org/img/self-logo.png" alt="Logo" width="200" height="80">
  </a>

<h3 align="center">Self Interpreter</h3>

<p align="center">
    A simple, easy-to-use, cross-platform interpreter for the Self language.
    <br />
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#authors">Authors</a></li>
        <li><a href="#acknowledgements">Acknowledgements</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a>
        <ul>
            <li><a href="#known-issues">Known Issues</a></li>
        </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
        <ul>
            <li><a href="#code-snippits">Code Snippits</a></li>
        </ul>
    </li>
    <li><a href="#video-demo">Video Demo</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## About The Project
<div id="about-the-project"></div>
<p>[Self](https://selflanguage.org/) is an object-oriented programming language designed around the use of prototypes, objects that are reused to derive behavior for other objects. It comes with its own environment, virtual machine, and GUI to execute in, the latter of which is defined in Self code. To learn more about how Self works, checkout out the [Self Handbook](https://handbook.selflanguage.org/2017.1/index.html).

As of the time of writing, the Self virtual machine is incapable of running directly on most modern operating systems such as Windows. To get working on an OS such as Windows, it requires users to set up a virtual machine that instead emulates older, 32-bit versions of Linux. For those who are interested in Self or adjacent languages like Smalltalk, this can be an unfortunate barrier of entry. This system, designed to parse and interpret Self inputs in a similar manner to the Self environment and virtual machine, is meant to address this problem. The project is built in Python, which is compatible with most modern platforms (e.g. Windows, Linux, macOS).

The Self Interpreter project is an interpreter for the Self language, built as a senior design project at the Rose-Hulman Institute of Technology. Its main purpose is to serve as an educational tool to inform computer science students of alternative programming paradigms but can also be used for most of your Self needs. The system is capable of reading in Self files from the existing Self implementation which is how most key objects (e.g. numbers, booleans, vectors, sets, dictionaries, etc) are built up.</p>

### Authors
<div id="authors"></div>

* [Achintya Gupta](https://www.linkedin.com/in/achintya-gupta-bb718517a/)
* [Luke McNeil](https://www.linkedin.com/in/luke-mcneil-9a9795196/)
* [Nathaniel Blanco](https://www.linkedin.com/in/nathaniel-blanco-06a694194/)
* [Jacob Pinney](https://www.linkedin.com/in/jacob-pinney/)

### Acknowledgements
<div id="acknowledgements"></div>

* [Professor Kim Tracy](https://www.linkedin.com/in/kimtracy/) - Advisor
* [Dr. Michael Hewner](https://hewner.github.io/) - Client

### Built With
<div id="built-with"></div>

* [python](https://www.python.org/)
* [ply](https://www.dabeaz.com/ply/)
* [kivy](https://kivy.org/)
* [pytest](https://pytest.org/)


<p align="right">(<a href="#top">back to top</a>)</p>

## Features
<div id="features"></div>

We have implemented support for the following features:
* Full-fledged parser
    * Capable of parsing valid Self input using Python LEX and YACC
* Robust Interpreter
    * Interprets core language features
    * Interprets classical algorithms such as the binary search algorithm
    * Interprets multi-line files written in Self (allows for code to be imported into the system)
        * The following original Self modules supported as a result of this feature include: block, boolean, collection, defaultBehavior, float, indexable, integer, list, nil, number, rootTraits, setAndDictionary, smallInt, string, vector
    * Can be run in parsing mode (to examine how a given input is parsed by the system) or interpreting mode (regular system without GUI)
* REPL
    * Read-eval-print loop for interfacing with the application through the console
* GUI
    * Built in the Self language, making it extensible by users
    * Powered by Kivy
* Compatibility with modern platforms

### Known Issues
<div id="known-issues"></div>

This project is a work in progress. As a result, you may experience some issues when working with the following:
* Resends in blocks
* Error handling functions
* Methods defined outside of objects (i.e. only using parentheses to define a method)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started
<div id="getting-started"></div>

### Prerequisites
<div id="prerequisites"></div>

The following must be installed with the given minimum versions.

* [python 3.7+](https://www.python.org/downloads/release/python-370/)
* ply
  ```sh
  pip install ply==3.11
  ```
* kivy
  ```sh
  pip install kivy==2.1.0
  ```
* pytest [optional: for tests only]
  ```sh
  pip install pytest==6.2.5
  ```
### Installation
<div id="installation"></div>

1. Clone the repo:
 * SSH:
   ```sh
   git clone git@github.com:pinneyja/self-interpreter.git
   ```
 * HTTP:
   ```sh
   git clone https://github.com/pinneyja/self-interpreter.git
   ```
2. Run the interpreter in CLI or GUI mode:
 * CLI: Run the interpreter command-line interface
   ```sh
   python src/REPL.py
   ```
 * GUI: Run the interpreter graphical user interface
   ```sh
   python src/GUI.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage
<div id="usage"></div>

1. To use the interpreter, boot up using the instructions <a href="#getting-started">above</a>.
2. While using the CLI, type commands into the console of your choice which will print the output.
3. While using the GUI, navigate using the on screen menus and evaluators.
4. To mass import Self code, add files to the `self_files/` directory. Then, use the `_RunScript` primitive to import your custom code!
5. Have fun and play around!

### Code Snippits
<div id="code-snippits"></div>

* Binary Search:
   ```sh
   lobby _AddSlots: 
   (| binarySearch: startVector Value: searchValue 
       = (| binarySearchHelper: vector Value: value FirstIndex: firstIndex LastIndex: lastIndex 
           = (| middleIndex. element |
               middleIndex: firstIndex + ((lastIndex - firstIndex) / 2).
               (firstIndex > lastIndex)
                           ifTrue: [^ -1]
                           False: [ ].
               element: (vector at: middleIndex IfAbsent: [error]).
               (value == element)
                   ifTrue: [^ middleIndex] 
                   False: [ 
                       ((value) < element)
                           ifTrue: [binarySearchHelper: vector Value: value FirstIndex: firstIndex LastIndex: (middleIndex - 1)] 
                           False: [binarySearchHelper: vector Value: value FirstIndex: (middleIndex + 1) LastIndex: lastIndex]])
           | binarySearchHelper: startVector Value: searchValue FirstIndex: 0 LastIndex: (startVector size) - 1)
   |)
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Video Demo
<div id="video-demo"></div>

Coming soon!

<p align="right">(<a href="#top">back to top</a>)</p>

## License
<div id="license"></div>

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>