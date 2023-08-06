from datetime import datetime, timedelta
from typing import Union, Tuple
from math import floor


class QuotaDuration:
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


QUOTA_UNLIMITED = -1


QUOTA_DURATION_SORTING = [QuotaDuration.SECOND, QuotaDuration.MINUTE, QuotaDuration.HOUR, QuotaDuration.DAY,
                          QuotaDuration.WEEK, QuotaDuration.MONTH, QuotaDuration.YEAR]

_duration_seconds = {
    QuotaDuration.SECOND: timedelta(seconds=1),
    QuotaDuration.MINUTE: timedelta(minutes=1),
    QuotaDuration.HOUR: timedelta(hours=1),
    QuotaDuration.DAY: timedelta(days=1),
    QuotaDuration.WEEK: timedelta(weeks=1),
}


class QuotaException(BaseException):
    def __init__(self, quota_remaining: Union[int, float] = None, quota_renew: datetime = None, custom_msg: str = None):
        super().__init__(custom_msg)
        self.quota_remaining: Union[int, float] = quota_remaining
        self.quota_renew: datetime = quota_renew

    def __str__(self):
        return f"Quota remaining: {self.quota_remaining} | " \
               f"Quota renews: {self.quota_renew.strftime('%Y-%m-%d %H:%M:%S')}"


class QuotaDefinition:
    def __init__(self, duration_type: str, credit_limit: Union[int, float], start_date: datetime):
        """
        Creates a new quota definition for a client and a specific interval
        :param duration_type: the duration type, see QuotaDuration class, specifies the duration for which the credit
        limit is valid for.
        :param credit_limit: the number of credits that the client can use in the provided duration type
        :param start_date: the start date, which will be used to calculate the current start/end of the renew interval.
        This can be a date far in the past, like 1st Jan 2020, the class will then compute the next renew datetime
        according to the duration type provided (second, minute, hour, day, week, month or year).
        """
        self.credits: Union[int, float] = credit_limit
        self.duration: str = duration_type
        self.start_date: datetime = start_date
        self.used_up: Union[int, float] = 0
        self.last_renew, self.next_renew = self._determine_renew_time()  # these are datetime objects

    def get_remaining_credits(self) -> Tuple[Union[float, int], datetime]:
        """
        Retrieves the number of remaining credits and the next time the used credits will be reset, depending on the
        provided duration type for this quota.
        :return:
        """
        if datetime.now() > self.next_renew:
            self.renew()

        if self.credits == QUOTA_UNLIMITED:
            return QUOTA_UNLIMITED, self.next_renew
        return self.credits - self.used_up, self.next_renew

    def _determine_renew_time(self) -> Tuple[datetime, datetime]:
        if self.duration == QuotaDuration.MONTH:
            # special handling for months
            now = datetime.now()
            # this is the start of the interval
            current_interval_start = now.replace(day=self.start_date.day)
            # go to next month
            if current_interval_start.month == 12:
                # handle december
                current_interval_end = current_interval_start.replace(month=1, year=current_interval_start.year + 1)
            else:
                # handle all other months
                current_interval_end = current_interval_start.replace(month=current_interval_start.month + 1)
            return current_interval_start, current_interval_end

        if self.duration == QuotaDuration.YEAR:
            # special handling for year
            now = datetime.now()
            current_interval_start = self.start_date.replace(year=now.year)
            # next year will be renewed
            current_interval_end = current_interval_start.replace(year=current_interval_start.year + 1)
            return current_interval_start, current_interval_end

        # all shorter interval types
        interval_length = _duration_seconds[self.duration].total_seconds()
        now = datetime.now()
        diff = (now - self.start_date).total_seconds()
        # find multiples of intervals passed since the start date
        multiples = floor(diff / interval_length)
        # find the next renew datetime
        current_interval_start = self.start_date + (multiples * _duration_seconds[self.duration])
        return current_interval_start, current_interval_start + _duration_seconds[self.duration]

    def renew(self):
        """
        Renews the credits used for this quota and sets the next renew datetime.
        """
        self.used_up = 0
        self.last_renew, self.next_renew = self._determine_renew_time()

    def check_credit_usage(self, required_credits: Union[int, float]):
        """
        This method will check if sufficient credits are available. If not, a QuotaException will be thrown holding the
        number of remaining credits and when the current quota is renewed. If the current quota duration is over, this
        method will also renew the quota for the next interval.
        :param required_credits: the number of required credits
        :raise: QuotaException in case the required_credits exceeds the available credits for this quota interval.
        """
        if datetime.now() > self.next_renew:
            # the current quota duration has expired
            self.renew()

        if self.credits == QUOTA_UNLIMITED:
            return

        # determine remaining credits
        remaining = self.credits - self.used_up
        if remaining < required_credits:
            raise QuotaException(remaining, self.next_renew)

    def use_credits(self, required_credits: Union[int, float]) -> Tuple[Union[int, float], datetime]:
        """
        This method will handle the usage of credits for this quota definition. It will deduct the credits from the
        remaining balance and return the remaining balance as well as the next renew datetime.
        :param required_credits: the number of required credits for an operation
        :return: the remaining credits after deduction of the required_credits and the next renew datetime for this
        quota.
        """
        # use up the credits
        self.used_up += required_credits
        # return remaining credits and renew
        if self.credits == QUOTA_UNLIMITED:
            return QUOTA_UNLIMITED, self.next_renew

        return self.credits - self.used_up, self.next_renew

    def init_used_up(self, used_up_credits: Union[float, int]):
        """
        Sets the initial amount of used up credits for the current renew interval. This is done on system restart, to
        prefill the quota definitions with the credits used up since the last renew before the system was restarted.
        :param used_up_credits: the number of credits used up already in the current interval (will just overwrite used
        credits value)
        """
        self.used_up = used_up_credits
