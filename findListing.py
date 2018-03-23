import csv
import MySQLdb

f = open("Registered_Business_Locations_-_San_Francisco.csv","r")

db = MySQLdb.connect(user="root", db='loco_sales')

reader = csv.reader(f)
first = True
for row in reader:
    if first:
        first = False
        continue
    sql = "insert into registered_biz(location_id,business_account,ownership_name,dba_name,street_address,city,state,source_zip,biz_start_date,biz_end_date,location_start_date,location_end_date,mail_address,mail_city,mail_zip,mail_state,naics_code,parking_tax,transient_occupancy_tax,lic_code,lic_code_description,supervisor,neighborhoods,business_corridor,business_location) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    c = db.cursor()
    c.execute(sql,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],
                   row[20],row[21],row[22],row[23],row[24]))
    db.commit()
    
