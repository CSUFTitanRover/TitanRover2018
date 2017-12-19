How we can use Deepstream
=========================

For the Controls Team, we can take advantage of using Deepstream by allowing multiple components to update the data store independently of each
other. As those updates occur, we can react to them and determine what needs to be done. There is obvisouly the requirement that each component 
must be able to have a network connection, however, this can be remedied by adding a network hat or some other solution. 

Here's an example configuration of a potential system layout:

.. image:: ../img/System-Layout-With-Deepstream-Example.png

Again, this is just an example configuration but the main point still sticks that we can use Deepstream to
make it easier to have direct updates across the entire system.