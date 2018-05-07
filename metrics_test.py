#!venv/bin/python
from metrics import Metrics
m = Metrics()
files = ['2010-13-080', '2010-00-072',
         '2010-00-094', '2010-26-075', '2010-58-011', '2010-08-078',
         '2010-94-034', '2010-71-034', '2010-40-008', '2010-08-069',
         '2010-92-061', '2010-70-013']
# tests the cutRecall
recall = m.cutRecall(sorted(files), '2010-001')
print(recall)
# tests the cutPrecision
precision = m.cutPrecision(sorted(files), '2010-001')
print(precision)
# tests the FMeasure
FMeasure = m.FMeasure(precision, recall)
print(FMeasure)
# tests the RRank1
RRank1 = m.RRank1(files, '2010-001')
print(RRank1)
# tests the RRank2
RRank2 = m.RRank2(files, '2010-001')
print(RRank2)
# tests the Aprecision
Aprecision = m.APrecision(files, '2010-001')
print(Aprecision)
