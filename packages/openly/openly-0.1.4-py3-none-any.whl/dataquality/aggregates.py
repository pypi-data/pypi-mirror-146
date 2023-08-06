from django.contrib.postgres.fields import JSONField
from django.db.models import Aggregate, Func, IntegerField

# Cast value for "percentage" values returned by PostgresQL
percentage = "Decimal(4,1)"
# Cast value for currency-type values returned by PostgresQL
dollars = "Decimal(15,2)"


class ArrayAgg(Aggregate):
    function = "ARRAY_AGG"
    template = "%(function)s(DISTINCT %(expressions)s)"

    def convert_value(self, value, expression, connection, context):
        if not value:
            return []
        return value


class ArrayLength(Func):
    function = "ARRAY_LENGTH"
    name = "Array_Length"
    template = "%(function)s(%(expressions)s, %(index)s)"


class ArrayFirst(Func):
    function = ""
    name = ""
    template = "(%(expressions)s) [1]"


class JSONObjectAgg(Aggregate):
    function = "JSONB_OBJECT_AGG"
    name = "JSONB_OBJECT_AGG"
    template = "%(function)s(%(expressions)s)"
    output_field = JSONField()


class Lower(Func):
    function = "LOWER"
    name = "Lower"
    template = "%(function)s(%(expressions)s)"


class SumOverPartition(Func):
    function = "SUM"
    name = "SumPartition"
    sum_fields = ""
    partition_fields = ""

    template = "%(function)s(%(sum_field)s) OVER (PARTITION BY %(partition_fields)s)"

    def __init__(self, *expressions, **extra):
        output_field = extra.pop("output_field", IntegerField())
        super(SumOverPartition, self).__init__(output_field=output_field)
        self.source_expressions = self._parse_expressions(*expressions)
        self.extra = extra

    def convert_value(self, value, expression, connection):
        if value is None:
            return 0
        return int(value)

    def as_sql(self, compiler, connection, function=None, template=None):
        connection.ops.check_expression_support(self)
        sql_parts = []
        params = []
        for arg in self.source_expressions:
            arg_sql, arg_params = compiler.compile(arg)
            sql_parts.append(arg_sql)
            params.extend(arg_params)
        if function is None:
            self.extra["function"] = self.extra.get("function", self.function)
        else:
            self.extra["function"] = function
        self.extra["expressions"] = self.extra["field"] = self.arg_joiner.join(
            sql_parts
        )
        template = template or self.extra.get("template", self.template)

        self.extra["partition_fields"] = ",".join(
            self.extra["expressions"].split(",")[1:]
        )
        self.extra["sum_field"] = self.extra["expressions"].split(",")[0]
        return template % self.extra, params
