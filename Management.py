from DB import *
from datetime import datetime

db = DB()


class Management():
    def get_all_licenses(self):
        return db.get_all_licenses()

    def find_record_data(self, text):
        return db.find_record_data(text)

    def check_license(self, license):
        x = db.check_license(license)
        if x:
            if x['time_out'] == "" and x['time_in'] != "":
                db.update_time(
                    license, x['time_in'], datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
            else:
                db.update_time(license, datetime.now().strftime(
                    "%H:%M:%S %d/%m/%Y"), "")
        return db.check_license(license)

    def add_new_user(self, name, dob, room, license):
        x = db.check_license(license)
        if x:
            msg = "Biển số đã tồn tại"
        else:
            db.add_new_user(name, dob, room, license)
            msg = "Thêm thành công"
        return msg

    def update_user(self, name, dob, room, license):
        x = db.check_license(license)
        if x:
            db.update_user(name, dob, room, license)
            msg = "Chỉnh sửa thành công"
        else:
            msg = "Biển số không tồn tại"
        return msg

    def delete_user(self, license):
        return db.delete_user(license)