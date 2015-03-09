from django.db.models import Lookup
from django.db.models.fields import Field

class EqualOrEmpty(Lookup):
    lookup_name = 'eoe'
    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params + rhs_params
        return '(%s = %s OR %s = "")' % (lhs, rhs, rhs), params
Field.register_lookup(EqualOrEmpty)

class LikeOrEmpty(Lookup):
    lookup_name = 'loe'
    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params + rhs_params
        return '(%s like %s OR %s = "")' % (lhs, rhs, rhs), params
Field.register_lookup(LikeOrEmpty)
