#!venv/bin/activate
from metrics import Metrics
m = Metrics()
files = ['2010-13-080', '2010-00-072',
         '2010-00-094', '2010-26-075', '2010-58-011', '2010-08-078',
         '2010-94-034', '2010-71-034', '2010-08-069',
         '2010-92-061', '2010-70-013']
print(m.cutPrecission(sorted(files)))
