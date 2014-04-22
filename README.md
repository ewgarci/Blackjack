Blackjack
===============

A Blackjack game using Python

Installation
------------

After cloning, create a virtual environment and install the requirements. For
Linux and Mac users:

    $ virtualenv venv
    $ source vevn/bin/activate
    (venv) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv venv
    $ venv\Scripts\activate
    (venv) $ pip install -r requirements.txt

Running
-------

To run the program use the following command:

    (venv) $ python blackjack.py

Feature
-------
* Support for multiple players on 1 computer (upto 6)
* Dealer strategy hits until his hand value is 17 or greater
* Basic Actions of hitting and standing
* Unit Tests with coverage

Future Work
-----------
* Integrate blackjack into online flask server with SocketIO
