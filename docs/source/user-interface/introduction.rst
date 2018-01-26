Introduction
============

Background
----------

In the years prior to the 2016 Titan Rover project, the UI was very bare bones and did not require a lot of intricate features.
However, starting with the 2016 Titan Rover project and due to the increasing dificulties of the URC guidelines, the 
UI needed to include useful features like an offline map for tracking the rover's position. The 2016 Titan Rover team
decided to build the 2016 platform using Node.js and that included the UI as well. At the time, the two main libraries being
considered were `React.js <https://reactjs.org/>`_ and `Angular.js <https://angularjs.org/>`_. After much consideration, 
it was decided to move forward with React because at the time Angular was going through some breaking changes to the main library. 

Abstract
--------

The user interface must be designed to be a soft real-time system. Meaning, losing some data packets being streamed from the
rover to the UI will not hurt the application. The user interface must also update as new data is received in order to 
display data in real-time. The maximum delay between new data packets being recieved in the UI should be less than 15ms. If
the delay time is longer than 15ms then user experience will degrade. The user interface must be customizable by the user so that
they can configure the layout of the UI in a way that is meaningful to them.