blackjack-flask
===============

A Blackjack game using Python and Flask

Installation
------------

After cloning, create a virtual environment and install the requirements. For
Linux and Mac users:

    $ virtualenv flask
    $ source flask/bin/activate
    (flask) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv flask
    $ flask\Scripts\activate
    (flask) $ pip install -r requirements.txt

Running
-------

To run the program use the following command:

    (flask) $ python blackjack.py

Build Issues
------------

Compiling with clang you may get the the following error when installing the greenlet dependency

	clang: error: unknown argument: '-mno-fused-madd' [-Wunused-command-line-argument-hard-error-in-future]

It can be fixed by using the following command

	ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install greenlet