__all__ = ('ProfileCreditScoringPoint',)

from expressmoney.api import *

SERVICE = 'profiles'


class ProfileCreditScoringCreateContract(Contract):
    pass


class ProfileCreditScoringReadContract(Contract):
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    is_default = serializers.BooleanField()
    score = serializers.DecimalField(max_digits=3, decimal_places=2)


class ProfileCreditScoringResponseContract(ProfileCreditScoringReadContract):
    pass


class ProfileCreditScoringID(ID):
    _service = SERVICE
    _app = 'credit_scoring'
    _view_set = 'profile_credit_scoring'


class ProfileCreditScoringPoint(ListPointMixin, ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = ProfileCreditScoringID()
    _read_contract = ProfileCreditScoringReadContract
    _create_contract = ProfileCreditScoringCreateContract
    _response_contract = ProfileCreditScoringResponseContract
