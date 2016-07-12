# insight_coding_challenge

I had some trouble with the run.sh file. I tested the solution with my own tests (in the tests.py and manually) and it was fine. However, when I tried to run run.sh, the first few times, it failed me on both tests, although I followed the instructions on how to try to structure the repo. On the second time, it said that my files were not there, and the next second, when I checked, they were gone.

Therefore, in the folder src, I uploaded venmo-trans.txt (the venmo input you provided), Extract_Info.py, which was the solution I wrote, output.txt, the output that my solution produced, and tests.py, which contains testing for the solution I wrote. I hope that is okay.

As I was working, I had my solution Extract_Info.py, venmo-trans.txt, and tests.py in the same folder, so they run under the assumption that these three things are in a folder together. The output txt is also written into the same folder that extract-info, tests, and venmo-trans.txt are written (which is in the src folder in this github repository).

I realized too late that another solution to the problem would be to build a balanced max heap from the incoming data payments, with the degree of the node attached to the nodes, and then use extract_max in order to find the median each time, as each JSON is processed.

My functions and classes are in the Extract_Info file. **In this file, I imported ast, datetime, and json.** I also have a tests file for testing purposes.

I have two classes, Node and Graph. My nodes are represented by the actor. My graph is represented as a dictionary where nodes are keys and values are lists of nodes that they are connected to.

I have several functions which assist the "main" function. These include get_information, which changes the textfile of JSON messages into a list of lists returned by get_information. Each of the lists in the master list, like the JSON messages contains an actor, target, and created time. 

There is also find_max_time, to find the larger of two times, and within_sixty, which determines if two times are within 60 seconds of each other. Find_median finds the median in a list.

Main is the main function which goes through the master list returned by get information and finds the median at each point in the list (after each payment is processed). The process of the function to find the median of the list is that it goes through each of the lists in the master list, where each list is a payment containing actor, target, and created time. In the list, the index for actor was always 0, for target, 1, and for time, 2, so that I could easily access them. From there, I check if the time of the payment is greater than the current maximum time, which I initialize to be “mindate” which occurs in MINYEAR of January 1st, where the hour, minute, and second fields are equal to zero. If the time of the payment is within 60 seconds of the maximum, then I create two nodes, of the actor and the target, add them to the graph if they are not already there, and connect them. Then I go through the list of nodes in the graph and remove all instances of any node that is no longer in the 60 second time window. I then go through the nodes again, getting the degrees of them and adding them to the list. In the end, I find the median of the list of degrees and return that after going through each payment.
