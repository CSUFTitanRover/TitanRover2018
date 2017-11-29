Why Use Deepstream
==================

As mentioned before, Deepstream can be considered a message broker and can deliver updates between different
applications. With the rover having sensors reading data and also needing that same data in different places
(e.g. different Python processes and the User Interface), then using Deepstream can allow us to access said data
with the same API. 

Use Case
--------

Here are 2 example use cases when using Deepstream or really any type of Message Broker. Let's start with a simple example. 

Simple Example
**************

Picture an Arduino with a temperature sensor, it has a .ino file written in C++ that reads the current temperature and then needs to send
that data to a Python process, let's call it PMain. PMain will receive that current temperature and compute an expected temperature for the next
reading through some magical algorithm. PMain will run on it's own computer separate from the ardunio. Once the expected temperature is computed, PMain needs to send both the current and next expected temperature
to a User Interface (Web Application) to display the data to the user. Figure 2 Illustrates the entire program layout.

.. image:: ../img/Use-Case-Simple-Example.png

**Figure 2. The layout of our 3 part program for our simple example.**

SO here's the big question... How are we suppose to transfer data from a C++ program to Python and then to a
Web Application?

You may jump to the answer that we can execute c++ inside a python program however that won't work because remember, the arduino and pyton programs
are running on their own boards. 