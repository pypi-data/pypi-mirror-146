from typing import List, Union, Dict, Tuple, Optional
from datetime import datetime
from flask import abort, make_response, Response
from frappyapibilling.usage_store import AbstractUsageStore
from frappyapibilling.quota_definitions import QuotaDefinition, QuotaException, QUOTA_DURATION_SORTING, QUOTA_UNLIMITED


class ApiBilling:
    def __init__(self, usage_store: AbstractUsageStore):
        self.clients: Dict[Union[str, int], List[QuotaDefinition]] = {}
        self.usage_store: AbstractUsageStore = usage_store

    def update_client_quotas(self, client_id, quota_definitions: List[QuotaDefinition]):
        # pre-flight check for duplicate durations
        used_durations = set()
        for quota in quota_definitions:
            if quota.duration in used_durations:
                raise ValueError(f"Duplicate duration type {quota.duration} detected.")
            used_durations.add(quota.duration)

        # store quotas with this instance
        self.clients[client_id] = list(sorted(quota_definitions,
                                              key=lambda x: QUOTA_DURATION_SORTING.index(x.duration)))

        # init the existing use per quota definition
        for quota in self.clients[client_id]:
            already_used = self.usage_store.get_total_usage(client_id, quota.last_renew, quota.next_renew)
            quota.init_used_up(already_used)

    def track_client_usage(self, client_id: Union[str, int], credits_used: Union[int, float] = 1, use_abort=True):
        if client_id not in self.clients:
            if use_abort:
                abort(403, description="You do not have any available quota")
            raise QuotaException(custom_msg="You do not have any available quota.")
        # check usage
        try:
            self._check_credits(client_id, credits_used)
        except QuotaException as qex:
            if use_abort is True:
                msg = f"You have only {qex.quota_remaining} credits remaining, but {credits_used} are required. " \
                      f"They will renew at {qex.quota_renew.strftime('%Y-%m-%d %H:%M:%S')}"
                abort(self.create_response_with_header(client_id, response_body=msg, status_code=429, exception=qex))
            else:
                raise qex

        # track credit usage
        self._track_usage(client_id, credits_used)

    def get_lowest_quota(self, client_id: Union[str, int]) -> Tuple[Union[float, int], datetime]:
        if client_id not in self.clients:
            return None, None

        lowest_value: Union[int, float] = None
        next_renew: datetime = None

        for quota in self.clients[client_id]:
            remaining, renew = quota.get_remaining_credits()
            if lowest_value is None:
                lowest_value = remaining
                next_renew = renew
            else:
                if remaining is QUOTA_UNLIMITED:
                    continue
                if lowest_value == QUOTA_UNLIMITED:
                    lowest_value = remaining
                    next_renew = renew
                elif remaining < lowest_value:
                    lowest_value = remaining
                    next_renew = renew

        return lowest_value, next_renew

    def create_response_with_header(self, client_id: Union[str, int], response_body,
                                    status_code: int = 200, exception: Optional[QuotaException] = None) -> Response:
        if exception is None:
            lowest_quota, next_renew_datetime = self.get_lowest_quota(client_id=client_id)
        else:
            lowest_quota, next_renew_datetime = exception.quota_remaining, exception.quota_renew

        response = make_response(response_body, status_code)
        if next_renew_datetime is None:
            # no quota available
            return response
        # set headers
        response.headers["X-RateLimit-Remaining"] = lowest_quota
        response.headers["X-RateLimit-Reset"] = round(next_renew_datetime.timestamp())
        return response

    def delete_client_usage(self, client_id: Union[str, int], start_datetime: Optional[datetime] = None,
                            end_datetime: Optional[datetime] = None):
        # delete from store
        self.usage_store.delete_client_usage(client_id, start_datetime, end_datetime)
        # check if client id is in cache
        if client_id not in self.clients:
            return
        # re-init cache (loads up2date usage from cache)
        quotas = self.clients[client_id]
        self.update_client_quotas(client_id, quotas)

    def _check_credits(self, client_id: Union[str, int], credits_required: Union[int, float]):
        """
        Finds the quota that has the fewest remaining credits. If a quota is found that has insufficient credits it is
        immediately returned.
        :param client_id:
        :param credits_required:
        """
        # no quota restrictions for this client
        definitions = self.clients.get(client_id, None)
        if definitions is None:
            return

        # check the quota definitions for this client
        for q_def in definitions:
            # this will throw a QuotaException, if insufficient credits are available
            q_def.check_credit_usage(credits_required)

    def _track_usage(self, client_id, credits_used):
        # no quota restrictions for this client
        definitions = self.clients.get(client_id, None)
        if definitions is None:
            return

        # check the quota definitions for this client
        for q_def in definitions:
            q_def.use_credits(credits_used)

        # store in usage store
        self.usage_store.track_usage(client_id, credits_used)
