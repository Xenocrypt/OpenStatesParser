OpenStatesParser
================

A Python module using the OpenStates API to generate and analyze current-term state legislative voting records.

To use it, import OpenStatesParser and run OpenStatesParser.VoteGenerator(state=YOURSTATE, chamber=YOURCHAMBER).

That will generate:

-OpenStatesParser.BillList, a list of bills in the current term.

-OpenStatesParser.VoteList, a list of contested votes in the current term.

-OpenStatesParser.VoteDict, a dictionary pairing an OpenStates legislative ID with the legislator's name, party, district, and a list of their votes in the same order as OpenStatesParser.VoteList.  'yes' is coded as '1', 'no' is coded as '6', and '9' indicates a legislator not listed as voting yes or no.  This coding more or less follows Simon Jackman's 'PSCL' package in R.

Note: OpenStates.Parser.VoteDict can take a long time to run, so it prints out how many bills remain to be checked, as well as how many contested votes there have been so far.

There are also the following functions:

-OpenStatesParser.Restart(), which deletes the above and allows OpenStatesParser.VoteGenerator to be run with a different state or chamber.

-OpenStatesParser.PeopleLike(ID, format=YOURFORMAT), which takes an OpenStates ID and generates either a dictionary or a list of legislators.  The default format is "list", and the list is sorted ascendinglyby the percentage of overlapping votes where they voted with the given legislator.  Legislators with no overlapping yes or no votes are given a "percentage" of -2.  You can also select the format "dict".

-OpenStatesParser.StateDifferenceFinder(ID1, ID2), which generates a list of votes where the legislators with OpenStates IDs "ID1" and "ID2" voted differently.

-OpenStatesParser.MatrixMaker(filename=YOURFILENAME, write=yes), which generates a roll call matrix with the information in OpenStatesParser.VoteDict.  If you specify write='yes', then the matrix is written using csv.writer to the specified file name, so the file name should end in '.csv'.

Note: I used my Sunlight apiikey as the default.  If you intend to use the library often, please get your own at http://sunlightfoundation.com/api/
