from datetime import datetime


class Rawdata:

    def build_servicing(self, data) -> None:
        self.id, self.vehicle, self.date, self.purpose, self.start, self.end, \
        self.mileageStart, self.mileageEnd, self.fuelAmount, self.fuelType, \
        self.driver =  data
        self.common_build()

    def build_trip(self, data) -> None:
        self.id, self.vehicle, self.date, self.destination, self.purpose, self.start, \
        self.end, self.stationary, self.mileageEnd, self.dist, self.driver, \
        self.approving, self.remarks =  data
        self.common_build()

    def common_build(self):
        self.timeStart = datetime.strptime(
            self.date.strip() + ' ' + self.start.strip(), '%d %b, %Y %H:%M')
        self.timeEnd = datetime.strptime(
            self.date.strip() + ' ' + self.end.strip(), '%d %b, %Y %H:%M')
        self.duration = self.timeEnd - self.timeStart
        del self.date, self.start, self.end
        self.purpose = self.purpose.upper()
