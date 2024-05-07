from enum import Enum


class Reward(Enum):
    REGISTRATION = "registration"
    SUBSCRIPTION = "subscription"
    CHECKIN = "checkin"
    CHECKIN_GAP_HOURS = "checkin_gap_hours"
    INVITATION = "invitation"
    REFERRER_PART = "referrer_part"
