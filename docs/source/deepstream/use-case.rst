Why Use Deepstream
==================

As mentioned before, Deepstream can be considered a message broker and can deliver updates between different
applications. With the rover having sensors reading data and also needing that same data in different places
(e.g. different Python processes and the User Interface), then using Deepstream can allow us to access said data
with the same API. 

Use Case
--------

Here is an example use case when using Deepstream or really any type of Message Broker. 

Simple Example
**************

Picture an Arduino with a temperature sensor, it has a .ino file written in C++ that reads the current temperature and then needs to send
that data to a Python process, let's call it PMain. PMain will receive that current temperature and compute an expected temperature for the next
reading through some magical algorithm. PMain will run on it's own computer separate from the ardunio. Once the expected temperature is computed, PMain needs to send both the current and next expected temperature
to a User Interface to display the data to the user. Let's assume the User Interface is a native desktop application written using C# and will
run on it's own laptop. Figure 2 Illustrates the entire program layout.

.. image:: ../img/Use-Case-Simple-Example.png

**Figure 2. The layout of our 3 part program for our simple example.**

So here's the big question... How are we suppose to transfer data from a C++ program to Python and then to a
User Interface?

You may jump to the answer that we can execute c++ inside a python program however that won't work because remember, the arduino and python programs
are running on their own boards.

As you can see, since every part of the entire program is separated physically from each other then this narrows down the solutions to our probelm.

Really, the only solution would be to transfer data over the network. Therefore, relying on a network connection to handle your data being transfered
from your Arduino to PMain and then to the User Interface. However, this means deciding what network protocol to use e.g. TCP or UDP.
TCP is good if you need to make sure your data gets sent from the Arduino to PMain, however, the messages may not be delivered very quickly with all the protocol overhead
with making it fail-safe. UDP is good choice if you don't care about losing data packets and just want it to arrive as quickly as possible.
There is also HTTP and `MQTT <http://mqtt.org/>`_ as a network protocol however the one important thing to keep in mind 
is: Once you get your data sent to PMain then how will you send it to the User Interface?

You see, we need to think about all of the moving parts in our example. Even though it's titled as a Simple Example it really is not. You may
think it's as easy as 1-2-3 but then you get hit with a baseball right to the gut. Welcome to the world of Titan Rover where things are much
more complicated then they seem.

Coming off our tangent, let's decide what to do for our network requirements. Let's use TCP for sending data from the Arduino to PMain since
we want to make sure we get every temperature reading. Then, we will use UDP for sending the computed and recorded data from PMain to the 
User Interface. Figure 3 Illustrates the updated program layout.


.. image:: ../img/Use-Case-Simple-Example-With-Network.png

**Figure 3. The updated layout of our 3 part program.**

 
