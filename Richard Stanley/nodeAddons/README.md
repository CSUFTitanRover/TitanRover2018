# NodeJS Addons
 This is and example of a basic nodeJs addon.

 Dependencies include:

  * NodeJs
  * npm
  * node-gyp
  * g++ compiler

Once you have those dependencies, you can test this build, by navigating to this directory, and running:

```sh
node-gyp configure build
```

The bindings file contains:

```json
{
  "targets": [
    {
      "target_name": "print",
      "cflags" : ["-std=c++11"],
      "sources": [ "print.cpp" ]
    }
  ]
}

```

The cflags: -std=c++11 argument will compile the code with the c++11 std library. This is needed because in the **print.cpp** file on line 17:

```cpp
for(unsigned i = 0; i < 1000; ++i) huge += to_string(i) + "\n";
```

we are using the **to_string()** function which comes with c++11 standard library.

Once the program is built with node-gyp, you can run the node application.  Look at the **print.js** to see
how the **node addon** is required (included) in the print.js app.

You can now run the addon with:

```shell
node print.js
```

The output will be a series of numbers for 0 - 999 separated by a new line.  This is the basics of how to 
compile c++11 for nodeJs applications.