import csv
import os

class generate_merge_report_camera:
    """
    Pleas pass the params to generate merge log petak"""
    def __init__(self,location,directory):
        self.location = location
        self.directory = directory

    def generate_merge_report_camera(location, directory):
        substring = "Camera Accuracy"
        headers = []
        rows_csv_merge = []

        for file in os.listdir(location + "\\Report Per Chunk"):
            move_folder = os.path.join(location,directory)
            #Create Prioritas Ketiga CSV
            csv_reader = csv.reader(open(os.path.join(move_folder,file)))
            header = next(csv_reader)
            headers.append(header)
            
            for row in csv_reader:
                rows_csv_merge.append(row)
            
        with open(location + "\\" + "test" + "_" + "prioritas_ketiga.csv","w",newline="") as q:
            csv2 = csv.writer(q, delimiter = ",")
            fields = ["Chunk Name","Keyid", "Camera Name", "Longitude", "Latitude", "Altitude", "Long Accuracy", "Lat Accuracy", "Alt Accuracy"]
            csv2.writerow(fields)

            for r in rows_csv_merge:
                csv2.writerow([r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8]])