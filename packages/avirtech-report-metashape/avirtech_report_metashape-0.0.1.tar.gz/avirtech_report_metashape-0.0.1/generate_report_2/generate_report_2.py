import csv

class generate_report_2:
    """
    Initiate generating report 2 which contains about information on those report, please pass the params include location and report_distinct"""
    def __init__(self, location, report_distinct):
        self.location = location
        self.report_distinct = report_distinct
    def create_report_log_petak(location,report_distinct):
        with open(location + "\\" + "Log Petak.csv","w",newline="") as f:
            csv2 = csv.writer(f, delimiter=",")
            csv2.writerow(["Chunk Name","Keyid","UAV Start","UAV End","Plant Date","Umur (Hari)","Plant Species","GSD","Filename","Image Accuracy"])
            for d in report_distinct:
                split_report = d.split("-")
                csv2.writerow([split_report[0],split_report[1],split_report[2],split_report[3],split_report[4],split_report[5],split_report[6],split_report[7],split_report[8],split_report[9]])
    