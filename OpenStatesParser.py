import json
import urllib2
import csv
APIKEY = '2e7d7ececfb742cf9f8394c300e98616'
VoteCodes = {'yes_votes': 1, 'no_votes': 6}
VoteList = []
VoteDict = {}
TotalVoteList = []
STATE = 'NY'
CHAMBER = 'upper'
def VoteGenerator(state=STATE, chamber=CHAMBER, apikey=APIKEY):
    try:
        BillList =  json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/?state=%s&chamber=lower&search_window=term&apikey=%s' % (state, apikey)))+json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/?state=%s&chamber=upper&search_window=term&apikey=%s' % (state, apikey)))
    except:
        BillList = []
        i = 1
        PartBillList = json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/?state=%s&chamber=lower&search_window=term&page=%s&per_page=10000&apikey=%s' % (state, i, apikey)))+json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/?state=%s&chamber=upper&search_window=term&page=%s&per_page=10000&apikey=%s' % (state, i, apikey)))
        while len(PartBillList) > 0:
            BillList = BillList+PartBillList
            i = i+1
            PartBillList = json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/?state=%s&chamber=lower&search_window=term&page=%s&per_page=10000&apikey=%s' % (state, i, apikey)))+json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/?state=%s&chamber=upper&search_window=term&page=%s&per_page=10000&apikey=%s' % (state, i, apikey)))
    Length = len(BillList)
    VotesLength = 0
    print 'Length of Bill List: ', Length
    for x in BillList:
        Votes = json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/%s/%s/%s/%s/?apikey=%s' % (state, urllib2.quote(x['session']), urllib2.quote(x['chamber']), urllib2.quote(x['bill_id']), apikey)))['votes']
        TotalVoteList = TotalVoteList+Votes
        if len(Votes) > 0:
            for Vote in Votes:
                if Vote['chamber'] == chamber and Vote['yes_count'] > 0 and Vote['no_count'] > 0:
                    VoteList.append(Vote)
                    for Legislator in list(Vote['yes_votes'])+list(Vote['no_votes']):
                        if Legislator['leg_id'] not in VoteDict:
                            VoteDict[Legislator['leg_id']] = {'Name': Legislator['name']}
                            for Trait in ['last_name', 'first_name', 'full_name', 'party', 'district']:
                                try: 
                                    VoteDict[Legislator['leg_id']][Trait] = json.load(urllib2.urlopen('http://openstates.org/api/v1/legislators/%s/?apikey=%s' % (Legislator['leg_id'], apikey)))[Trait]      
                                except:
                                    VoteDict[Legislator['leg_id']][Trait] = 'NA' 
                    VotesLength = VotesLength+1
        Length = Length-1
        print 'Bills remaining: %s, Votes So Far: %s ' % (Length, VotesLength)  
    for i in range(len(VoteList)): 
        Vote = VoteList[i]
        for Option in VoteCodes:
            for Legislator in Vote[Option]:
                if 'Votes' not in VoteDict[Legislator['leg_id']]:
                    VoteRow = []
                    while len(VoteRow) < VotesLength:
                        VoteRow.append(9)
                    VoteDict[Legislator['leg_id']]['Votes'] = VoteRow
                VoteDict[Legislator['leg_id']]['Votes'][i] = VoteCodes[Option]
def Restart():
    global VoteList
    VoteList = []
    global VoteDict
    VoteDict = {}
    global TotalVoteList
    TotalVoteList = []
def StateDifferenceFinder(j, k):
    if j in VoteDict and k in VoteDict:
        First = VoteDict[j]['Votes']
        Second = VoteDict[k]['Votes']
    else:
        print 'One of those is not in the current VoteDict'
        return
    Difference = []
    for L in range(len(VoteList)):
        Max = max(First[L], Second[L])
        Min = min(First[L], Second[L])
        if Max-Min == 5:
            Difference.append(VoteList[L]['vote_id'])
    return Difference  
FILENAME = 'VoteMatrix.csv'  
RESULT = 'list'
def PeopleLike(i, format=RESULT):
    DifferenceDict = {}
    DifferenceList = []
    for x in VoteDict:
        DifferenceDict[x] = [0, 0]
    for L in range(len(VoteList)):
        TheirVotes = VoteDict[i]['Votes'][L]
        for x in VoteDict:
            if TheirVotes !=9 and VoteDict[x]['Votes'][L] != 9:
                if VoteDict[x]['Votes'][L] == TheirVotes:
                    DifferenceDict[x][0]=DifferenceDict[x][0]+1
                else:
                    DifferenceDict[x][1]=DifferenceDict[x][1]+1 
    for x in DifferenceDict:
        if DifferenceDict[x][0]+DifferenceDict[x][1] > 1:
            DifferenceList.append([x, VoteDict[x]['Name'], VoteDict[x]['party'], DifferenceDict[x][0], DifferenceDict[x][1], float(DifferenceDict[x][0])/(float(DifferenceDict[x][1])+float(DifferenceDict[x][0]))])
        else:
            DifferenceList.append([x, VoteDict[x]['Name'], VoteDict[x]['party'], DifferenceDict[x][0], DifferenceDict[x][1], -2])
    DifferenceList = sorted(DifferenceList, key=lambda Leg:Leg[5])
    if format == 'list':
        return DifferenceList
    if format == 'dict':
        return DifferenceDict
    if format not in ['list', 'dict']:
        return DifferenceList
        print 'I don\'t know what format you meant, but here\'s a list.'
YES = 'yes'
def MatrixMaker(filename=FILENAME, write=YES):
    FirstRow = ['Leg_ID', 'Last_Name', 'First_Name', 'District', 'Party']
    for x in VoteList:
        FirstRow.append(x['vote_id'])
    Matrix = [FirstRow]
    for x in VoteDict:
        Matrix.append([x, VoteDict[x]['last_name'], VoteDict[x]['first_name'], VoteDict[x]['district'], VoteDict[x]['party']]+VoteDict[x]['Votes'])
    if write=='yes':
        csv.writer(open(filename, 'wb')).writerows(Matrix)
    return Matrix
