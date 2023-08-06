"""
Data attributes for events within enterprise-access.
"""

import attr

# TODO (EVENT BUS):
# Move the CouponCodeRequestData class to openedx_events


@attr.s(frozen=True)
class CouponCodeRequestData:
    """
    Attributes defined for a CouponCodeRequest object.
    """

    uuid = attr.ib(type=str)
    lms_user_id = attr.ib(type=int)
    course_id = attr.ib(type=str)
    enterprise_customer_uuid = attr.ib(type=str)
    state = attr.ib(type=str)
    reviewed_at = attr.ib(type=str)
    reviewer_lms_user_id = attr.ib(type=int)
    coupon_id = attr.ib(type=int)
    decline_reason = attr.ib(type=str, default=None)
    coupon_code = attr.ib(type=str, default=None)


class CouponCodeRequestEvent:
    """
    Coupon code request events to be put on event bus.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a CouponCodeRequestEvent.
        """
        self.uuid = kwargs['uuid']
        self.lms_user_id = kwargs['lms_user_id']
        self.course_id = kwargs['course_id']
        self.enterprise_customer_uuid = kwargs['enterprise_customer_uuid']
        self.state = kwargs['state']
        self.reviewed_at = kwargs['reviewed_at']
        self.reviewer_lms_user_id = kwargs['reviewer_lms_user_id']
        self.coupon_id = kwargs['coupon_id']
        self.coupon_code = kwargs['coupon_code']

    AVRO_SCHEMA = """
        {
            "namespace": "enterprise_access.apps.subsidy_request",
            "name": "CouponCodeRequestEvent",
            "type": "record",
            "fields": [
                {"name": "uuid", "type": "string"},
                {"name": "lms_user_id", "type": "int"},
                {"name": "course_id", "type": "string"},
                {"name": "enterprise_customer_uuid", "type": "string"},
                {"name": "state", "type": "string"},
                {"name": "reviewed_at", "type": ["string", "null"]},
                {"name": "reviewer_lms_user_id", "type": ["int", "null"]},
                {"name": "coupon_id", "type": ["int", "null"]},
                {"name": "coupon_code", "type": ["string", "null"]}
            ]
        }
    """

    @staticmethod
    def from_dict(dict_instance, ctx):  # pylint: disable=unused-argument
        """
        Create an instance of CouponCodeRequestEvent from dict.
        """
        return CouponCodeRequestEvent(**dict_instance)

    @staticmethod
    def to_dict(obj, ctx):  # pylint: disable=unused-argument
        """
        Convert an instance of CouponCodeRequestEvent to dict.
        """
        return {
            'uuid': obj.uuid,
            'lms_user_id': obj.lms_user_id,
            'course_id': obj.course_id,
            'enterprise_customer_uuid': obj.enterprise_customer_uuid,
            "state": obj.state,
            "reviewed_at": obj.reviewed_at,
            "reviewer_lms_user_id": obj.reviewer_lms_user_id,
            "coupon_id": obj.coupon_id,
            "coupon_code": obj.coupon_code
        }
