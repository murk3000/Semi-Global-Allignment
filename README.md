# Semi-Global-Allignment
Using the Smith-Waterman Algorithm to create a semi-global alignment using only the forward pass

## FAQs

### How to use?
Simply go to the user input section, enter sequences and gap penalty, and run the python code!

### What the algorithm does?
It creates a 2D matrix that shows the maximum score possible for the pairwise allignment of two proteins.
Ideally, in a semi-global allignment you would compute forward and backward passes to get the best possible allignment. In this you only go through a forward pass of the proteins. With some basic understanding of the code, one could easily modify this to do so.

### Can local or global allignment be done with this?
Yes! By following the comments you can insert peices of code that would do so!
