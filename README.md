# Python for Astronomy — A talk at the Observational Techniques Workshop 2018

Observational Techniques Workshop at the AAO, 30 April to May 3, 2018.

Workshop website: [https://www.aao.gov.au/conference/OTW2018]()



## Pythonyp Overview

- Python, Numpy, Scipy and Astropy
- Python 2 vs Python 3: the [clock](https://pythonclock.org/) is ticking! If you're new to Python, you should use Python 3 and not look back!



## Advertisement for previous talk at OTW2016

For those interested, I gave a talk at the OTW2016 on using Python to access data in various online repositories. Specifically, it covers:

- How to take the data from a table in a published paper and plot it in Python *without copying the data from the PDF, typing, or even having to handle the data at all*.
- How to access data from the Gemini archive from within Python.

The talk is an exercise in just how many tools there are for accessing data relevant for astronomy and how easy they are to use.

[Notes from the talk](https://github.com/astrogreen/obs_techniques_workshop/blob/master/otw2016/Notes.md)

[Video of the talk](https://youtu.be/4t7XaY-FHgs)

## Interlude in Software Engineering and Computer Science

### Abstraction

Abstraction is an idea of hiding implementation details behind an interface. While few people could describe in detail what happens when one starts a modern car. However, when handed the key, almost anyone could get in the car and start it. This is an abstraction. The interface is the key and ignition slot. Virtually all cars have the same interface (okay some cars have the slot on the left side of the column instead of the right, and increasingly, push button start). The key and the ignition slot are an abstraction that hide the details of what happens under the bonnet (hood) of a modern car.

In software, abstractions serve two purposes: they allow the details of an implementation not relevant to an end user to be hidden from the user. These are often called "black boxes". This hiding is not an attempt to deceive, it is an attempt to simplify. We can wrap up a bunch of code in a function called `sort` and, generally, anyone reading the code will have a pretty good idea what `sort` does. This is far easier to read than if the entire content of the `sort` function was written out in the code every time it was needed.

The second purpose of abstraction in software is to enable reuse of functionality. The `sort` function can be used in many places and situations without modification, so it can easily be re-used. Similarly, because there is an "interface" between `sort` and the code that is calling it, if, in the future, someone invents a better way of sorting, this new function can be exchanged with the existing function without needing to rewrite any of the code that calls `sort`.

To consider an example in astronomy (which is relevant to this talk), consider a data reduction manager that helps one to reduce a set of astronomical observations. At the highest level, if good abstraction is used, then the same manager could be used to reduce data from many different telescopes (as the typical calibration sequences, etc, are similar or the same between telescopes), requiring only the definition of the observation be changed between telescopes.

Good use of abstraction also helps to make code more readable.

### Readable code

Code readability can mean a lot of things. Perhaps the most important thing is that your code be readable by the future you. How often have to written a complicated bit of code to reduce some data, only to come back after the long weekend out sailing to discover that the brilliant code you wrote last week is impenetrable, and you can't fix the seemingly simple but infuriating bug it has developed?

Another reason to think about making your code readable is so that your collaborators can read it easily and help you to ensure that it is correct. The more readable the code is, then typically the more obvious errors in logic and bugs in implementation will be. Remember, we all want our science to be repeatable!

So what makes code readable? Well, there are lots of references on the internet, so just go have a look. A few resources I recommend having a look at:

- https://simpleprogrammer.com/what-makes-code-readable-not-what-you-think/
- https://www.python.org/dev/peps/pep-0008/, especially the section [A Foolish Consistency is the Hobgoblin of Little Minds](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds)
- [StackOverflow Answer on Code Readability](https://stackoverflow.com/a/550920/1970057)

Also, consider this treatise on how to write impenetrable code (note the original has been hacked, and is unsafe, so the link below is to the archived version):

https://web.archive.org/web/20120112000640/http://thc.org/root/phun/unmaintain.html

### Testing

People talk a lot about automated code testing, and it usually sounds like a good idea in principle. But how do you find the time to write tests when you also need to get the paper done and prepare for next week's observing? I struggled with this problem for ages.

Ultimately, I found the answer to be in how I approach developing code. I noticed that when developing code, I was constantly loading the code into the python interpreter and running it to check if it got the answer I expect. This is very quick if only a single line must be executed each time I need to check my code. But often one finds that there are many steps required to set up the test each time. Imagine testing a data reduction step. Each time the code changes, I need to restart python, load the fits file, and pre-populate a few different variables before I can get the result I need to check. For example, maybe I'm trying to make sure that my reduction code returns data with the correct orientation:

```python
from astropy.io import fits

from my_reduction import do_reduce

filename = "22apr10004.fits"
data = fits.open(filename)[0].data
flat_filename = "22apr10005.fits"

result = do_reduce(filename, flat_filename)

print(result.shape)
```

I think I want `result.shape` to have the larger number in the first slot, probably something like (2048, 819).

Rather than reload python and paste this bit of code in every time, instead I could write a test to do this. Using a python package called `pytest`, this can be really quite easy. I create a new file called `test_my_reduction.py` with this in it:

```python
import pytest

from astropy.io import fits

from my_reduction import do_reduce


def test_dimensions_in_correct_order()
    filename = "22apr10004.fits"
    data = fits.open(filename)[0].data
    flat_filename = "22apr10005.fits"

    result = do_reduce(filename, flat_filename)

    print(result.shape)
    
    assert False
```

I can then run this test from the command line with a single command: `pytest test_my_reduction.py`. As written above, this test will "fail", and the value of `result.shape` will be printed to the terminal. When I figure out what answer I think I should get, I can then replace `assert False` with the actual test I want, such as `assert result.shape[0] > result.shape[1]`. More tests can be included in the function with additional `assert` statements.

I find that this actually accelerates my development, which is a very iterative process anyway (write code, test, repeat). If you're doing something repetitively, why not automate it!



There are many ways to do testing, and other methods may be more useful for you or your situation. In particular so called "regression testing" can be very useful for understanding how changes to e.g. a data analysis pipeline changes the results. Tests can confirm that only the things you're expecting to change really do.



## Writing a data reduction manager in Python

### Preliminaries

Integrated development environments (IDEs) are very helpful for writing code. Currently, [**PyCharm**](https://www.jetbrains.com/pycharm/) is a very good, free IDE for Python. There are many others as well (e.g. Spyder). What sets PyCharm apart is that it is part of a much larger suite of IDEs that is available as a commercial product, so the free community edition of PyCharm benefits from a lot of expensive development.

Version control is really a good idea. And I don't mean just appending `v1`, `v2`, `v3`… to the filenames, though that is still better than nothing. `git` is very popular, but unfortunately suffers from a somewhat poorly designed user interface (command names are rarely intuitively named, etc.). Mercurial (`hg`) is typically more intuitive, but is less popular. As much as I don't like it, I would probably recommend `git` today, but the choice is yours. For either tool, there are great GUI tools ([SourceTree](https://www.sourcetreeapp.com/) is a good example), which can greatly ease the learning curve.

### Description of the problem

We would like to automate the execution of the 2dfdr data reduction system. We've already gotten some help from someone else on how 2dfdr can be run from the command line, and we've worked through a few by hand to make sure we have a picture of how this works before starting.

The description of the process is here: [Data Reduction Process.md](https://github.com/astrogreen/obs_techniques_workshop/blob/master/Data%20Reduction%20Process.md)

### The Source

The code for this manager is included in this repository. The current final version is in the `master` branch, which can easily be downloaded from the green button at the top right of this page [https://github.com/astrogreen/obs_techniques_workshop](). If you would like to see the code as I developed in stages during the talk, you can find the individual versions in the repository as tags:

- [`talk1`](https://github.com/astrogreen/obs_techniques_workshop/blob/talk1/data_reducer.py): Once the initial code design has been sketched out
- [`talk2`](https://github.com/astrogreen/obs_techniques_workshop/blob/talk2/data_reducer.py): Observation class is fleshed out, and we've written the `import_new_observation` function to bring these observations into the manager. This function also also handling identifying which grouping each observation belongs to.
- [`talk3`](https://github.com/astrogreen/obs_techniques_workshop/blob/talk3/data_reducer.py): The `ReductionGrouping` class is fleshed out to actually call the external reduction in 2dfdr using the command line function `aaorun`.
- [`talk4`](https://github.com/astrogreen/obs_techniques_workshop/blob/talk4/data_reducer.py):  The Manager class is updated to accept a string filename to the `import_new_observation` function to make it simpler to bring new data into the manager.
- [`talk5`](https://github.com/astrogreen/obs_techniques_workshop/blob/talk5/data_reducer.py): Includes the necessary changes to reflect that the `plate_id` was ultimately insufficient to identify reduction groupings (causing red and blue arms to be reduced using the same calibrations).

With each version, look at the corresponding `test_data_reducer.py` file for examples of how the code is actually used at each stage. (Apologies I didn't get to go into what it actually looked like from the user's perspective in my talk.) The final interface to reduce a whole set of data looks something like this:

```python
from glob import glob  # Returns a list of all filenames matching the pattern
from data_reducer import *

mngr = SAMIReductionManager()

# Assuming all files in the example dataset have been put in the 
# same directory together, which is the current working directory:

all_files = glob("*.fits")
print(all_files)
for f in all_files:
    mngr.import_new_observation(f)

mngr.reduce_all()
```

If you have 2dfdr installed and `aaorun` is available on the command line, then this will actually reduce your data. If you don't then it will just print out the commands that would be used.



# Questions



