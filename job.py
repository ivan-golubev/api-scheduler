from datetime import datetime, timedelta


class Job():
    def __init__(self, cron_str):
        cron = cron_str.split()
        if len(cron) < 3:
            raise Exception('Invalid input command format')
        self.m, self.h, self.cmd = Job.validate(cron[0]), Job.validate(cron[1]), cron[2]

    def __repr__(self):
        return "{} {} {}".format(self.m, self.h, self.cmd)

    @staticmethod
    def validate(i):
        if i == '*':
            return '*'
        else:
            try:
                return int(i)
            except ValueError:
                raise Exception('Invalid input command format')

    def get_next_execution(self, h, m):
        next_h = 0
        next_m = 0
        when = 'undefined'

        if self.h == '*' and self.m == '*':
            d = time_custom(1, h, m) + timedelta(minutes=1)
            next_h, next_m, when = unpack_date(d)
        elif self.h == '*':
            d = time_custom(1, h, self.m)
            if m > self.m:
                d += timedelta(hours=1)
            next_h, next_m, when = unpack_date(d)
        elif self.m == '*':
            d = 0
            if h < self.h:
                d = time_custom(1, self.h, 0)
            elif h == self.h and m < 59:
                d = time_custom(1, h, m) + timedelta(minutes=1)
            else:
                d = time_custom(2, self.h, 0)
            next_h, next_m, when = unpack_date(d)
        else:
            next_h = self.h
            next_m = self.m
            when = 'tomorrow' if time_custom(1, next_h, next_m) < time_custom(1, h, m) else 'today'
        return '{:0>2}:{:0>2} {} {}'.format(next_h, next_m, when, self.cmd)


def unpack_date(d):
    return d.hour, d.minute, 'tomorrow' if d.day > 1 else 'today'


def time_custom(d, h, m):
    return datetime(2000, 1, d, h, m)
