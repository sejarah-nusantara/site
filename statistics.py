import sys
sys.path.append('./import_scripts')
from common import sh
ls = sh('git log | grep Date')
ls = ls.split('\n')
for x in ls: print x

print 'SINCE FIRST COMMIT:'

print '-' * 20
print len(ls), 'commits'
print len(ls) * 2, 'hours, given 2 hours per commit'
ls = [x[0:18] for x in ls]


ls = set(ls)
ls = list(set(ls))

print len(ls), 'days'
print len(ls) * 6, 'hours in 6 hour workdays'

print '-' * 20

print 'SINCE 1 OCTOBER:'

ls = sh('git log --since={2012-10-01} | grep Date')
ls = ls.split('\n')
print '-' * 20
print len(ls), 'commits'
print len(ls) * 2, 'hours, given 2 hours per commit'
ls = [x[0:18] for x in ls]

ls = set(ls)
ls = list(set(ls))

print len(ls), 'days'
print len(ls) * 8, 'hours in 8 hour workdays'

print '-' * 20

ls = sh(r"""git log --numstat --pretty="%H"  | awk 'NF==3 {plus+=$1; minus+=$2} END {printf("+%d, -%d\n", plus, minus)}'""")
print ls
added, deleted = ls.split(',')
added = int(added)
deleted = int(deleted.strip()[1:])
print '%s lines added' % added
print '%s lines deleted' % deleted
print 'total lines', added - deleted
#print (added-deleted) * 1, 'hours at 1 hour per line' 
print '-' * 20

print 'Original offerte'
print 'beta-1:  64 hours - oktober 1' 
print 'beta-2: 360 hours' 


