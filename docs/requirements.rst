=============
Actions Overview
=============
Actions are triggered as a result of an event. They are defined by an admin
and can best characterised as, "When an event occurs, do such and such action.
Actions are given unique names and descriptions.

    =============
    Prerequsites
    =============
    SQLAlchemy

==============
Actions
==============
Actions invoke a function (class method?) written by a programmer. There are two
builtin actions: email and alert. Both are html templates that are rendered using
Jinja2.

Code that executes actions is registered.

==============
Events
==============
Events occur as a result of a create, update, or deletion of a database record.

They are also periodic similar to 
