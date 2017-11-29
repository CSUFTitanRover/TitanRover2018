What Is Deepstream
==================

There are similarities that can be drawn between Deepstream and other products like Firebase, Redis, etc.
Deepstream supports concepts like pub/sub, rpcs, and data-syncing. 
It can be considered that Deepstream acts as a message broker, however, this 
`blog post <https://deepstreamhub.com/blog/realtime-framework-overview/>`_ explains the comparisons in
much more detail. 

Message Broker
--------------
A message broker can be defined as a physical component that handles the communication between applications. Instead of communicating with each other, applications communicate only with the message broker. An application sends a message to the message broker, providing the logical name of the receivers. The message broker looks up applications registered under the logical name and then passes the message to them.
Figure 1 illustrates this configuration.

.. image:: ../img/message-broker-example-diagram.gif

**Figure 1. A message broker mediating the collaboration between participating applications**

Expanding on the idea of Deepstream acting as a message broker, with this in mind, one can develop a product with
multiple moving parts written in different programming languages and still have things working together. A message
broker allows you to treat data and events from a language agnostic standpoint.

Data Store
----------
Deepstream offers a `in-cache data store <https://deepstreamhub.com/tutorials/guides/records/>`_ that can hold all types of data.

- Numbers (Integers/Doubles)
- Strings
- Objects
- Lists

Pub/Sub
-------
Deepstream offers the ability of a `publish and subscribe event pattern <https://deepstreamhub.com/tutorials/guides/events/>`_.
Clients can publish data through the deepstream system and any clients subscribed can receive that data. 

RPC
---
Deepstream offeres `remote procedural call (RPC) <https://deepstreamhub.com/tutorials/guides/remote-procedure-calls/>`_
which are equivalent to a request-response pattern. 

Data-Sync
---------
Deepstream offeres data-syncing when items/records are updated in your data store.
