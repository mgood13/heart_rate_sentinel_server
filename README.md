# heart_rate_sentinel_server
Heart Rate Sentinel Server Project Repository

This server is intended to take in patient information from a program and then store it in a dictionary
that is contained on the server. This allows for continual updating and adjusting by the user. The code can
be run in a manner that is consistent with the one found in the file ServerCall.py. This file is intended
to be used to prime the server to perform the testing. But it also serves as a template.
The testing file contains all the functions used to test the server. In reality pretty much every single "function"
that the server performs was controlled by an app function and then another function that actually does any
fetching or calculating that needs to be done. I opted to run tests on the app functions and those served to test
the calculating functions. This is because the app functions couldn't actually work without the other functions
working properly and thus it would be reasonable that the two could be grouped together. 