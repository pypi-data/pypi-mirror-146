Cova Dispensary POS Audit Tool
===================

An inventory audit tool for speeding up inventory and avoiding errors that occur during processing. This tool will allow
users to complete inventory counts with a simple workflow that remedies user error.


Installation and Usage
-----
``` bash
$ pypi install audit-tools
```

``` pyhton
    >>> from audit_tools import SessionManager
    >>> session = SessionManager('/path/to/products.csv')
    ...
    >>> session.count_product('F7X6A7', 20)
    >>> session.reduce_product('F7X6A7', 3)
    ...
    >>> session.shutdown()
```


Problems
--------
All of the problems that we encounter while processing inventory data during an audit.

* Extremely slow
* Miscounts often
* Redundant item checks
* Manual Data Entry

Solutions
---------
Our ideas for solution implementations for fixing these problems so that an Audit can be completed successfully with
accuracy and speed.

- #### Session Manager
    - Allows users to start a new session with a products csv or xlsx file. The session manager will process all incoming
    products and append them to the sessions DataFrame, at the end of the session the session manager will parse all of
    the data in the session, complete variance calculations, raise any alerts, and save the session to the updated csv
    or xlsx file.


- #### Scan & Count
    - Allows users to scan a SKU and count the number of products to update the session file.


- #### Scan & Edit
    - Allows user to scan a SKU adn manage the data entry for a specified product in the session.


- #### Receipt Parser
    - Allows user to uploada receipt scan and the system will parse the receipt and update the session file.

Feature List
------------
This list will include all the features, current and future.

| Features        |   Working Status   |
|-----------------|:-------------------:|
| Session Manager |   In Development   |
| Scan & Count    |      Planned       |
| Scan & Edit     |      Planned       |
| Receipt Parser  |      Planned       |