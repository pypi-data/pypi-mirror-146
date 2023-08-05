from sigma.conversion.state import ConversionState
from sigma.types import re, SigmaString
from sigma.rule import SigmaRule
from sigma.conversion.base import TextQueryBackend
from sigma.conversion.deferred import DeferredQueryExpression, DeferredTextQueryExpression
from sigma.conditions import ConditionFieldEqualsValueExpression, ConditionOR, ConditionAND
from sigma.types import SigmaCompareExpression
from sigma.exceptions import SigmaFeatureNotSupportedByBackendError
from typing import ClassVar, Dict, List, Tuple, Union

class InsightIDRBackend(TextQueryBackend):
    """InsightIDR LEQL backend."""
    group_expression : ClassVar[str] = "({expr})"

    or_token : ClassVar[str] = "OR"
    and_token : ClassVar[str] = "AND"
    not_token : ClassVar[str] = "NOT"
    eq_token : ClassVar[str] = "="

    icontains_token: ClassVar[str] = "ICONTAINS"
    icontains_any_token: ClassVar[str] = "ICONTAINS-ANY"
    icontains_all_token: ClassVar[str] = "ICONTAINS-ALL"

    istarts_with_token: ClassVar[str] = "ISTARTS-WITH"
    istarts_with_any_token: ClassVar[str] = "ISTARTS-WITH-ANY"

    str_quote : ClassVar[str] = '"'
    str_single_quote : ClassVar[str] = "'"
    str_triple_quote = '"""'
    escape_char : ClassVar[str] = "\\"
    wildcard_multi : ClassVar[str] = "*"
    wildcard_single : ClassVar[str] = "*"

    re_expression : ClassVar[str] = "{field}=/{regex}/i"
    re_escape_char : ClassVar[str] = "\\"
    re_escape : ClassVar[Tuple[str]] = ('"')

    cidr_expression : ClassVar[str] = "{field} = IP({value})"

    compare_op_expression : ClassVar[str] = "{field} {operator} {value}"
    compare_operators : ClassVar[Dict[SigmaCompareExpression.CompareOperators, str]] = {
        SigmaCompareExpression.CompareOperators.LT  : "<",
        SigmaCompareExpression.CompareOperators.LTE : "<=",
        SigmaCompareExpression.CompareOperators.GT  : ">",
        SigmaCompareExpression.CompareOperators.GTE : ">=",
    }

    field_null_expression : ClassVar[str] = "{field} = null"

    field_in_list_expression : ClassVar[str] = "{field} IIN [{list}]"
    field_icontains_any_expression : ClassVar[str] = "{field} ICONTAINS-ANY [{list}]"
    field_icontains_all_expression : ClassVar[str] = "{field} ICONTAINS-ALL [{list}]"
    field_istarts_with_any_expression : ClassVar[str] = "{field} ISTARTS-WITH-ANY [{list}]"
    list_separator : ClassVar[str] = ", "

    unbound_value_str_expression : ClassVar[str] = '"{value}"'
    unbound_value_num_expression : ClassVar[str] = '{value}'
    unbound_value_re_expression : ClassVar[str] = '{value}'
    no_case_str_expression: ClassVar[str] = "NOCASE({value})"

    def get_quote_type(self, string_val):
        """Returns the shortest correct quote type (single, double, or trip) based on quote characters contained within an input string"""
        if '"' and "'" in string_val:
            quote = self.str_triple_quote
        elif '"' in string_val:
            quote = self.str_single_quote
        else:
            quote = self.str_quote

        return quote

    def basic_join_or(self, cond, state):
        """Default conversion of OR conditions"""
        if self.token_separator == self.or_token:   # don't repeat the same thing triple times if separator equals or token
            joiner = self.or_token
        else:
            joiner = self.token_separator + self.or_token + self.token_separator

        result = joiner.join((
                converted
                for converted in (
                    self.convert_condition(arg, state) if self.compare_precedence(ConditionOR, arg.__class__)
                    else self.convert_condition_group(arg, state)
                    for arg in cond.args
                )
                if converted is not None and not isinstance(converted, DeferredQueryExpression)
            ))
        return result

    def basic_join_and(self, cond, state):
        """Default conversion of AND conditions"""
        if self.token_separator == self.and_token:   # don't repeat the same thing triple times if separator equals and token
            joiner = self.and_token
        else:
            joiner = self.token_separator + self.and_token + self.token_separator

        result = joiner.join((
                converted
                for converted in (
                    self.convert_condition(arg, state) if self.compare_precedence(ConditionAND, arg.__class__)
                    else self.convert_condition_group(arg, state)
                    for arg in cond.args
                )
                if converted is not None and not isinstance(converted, DeferredQueryExpression)
            ))
        return result


    def convert_condition_field_eq_val_str(self, cond : ConditionFieldEqualsValueExpression, state : ConversionState) -> Union[str, DeferredQueryExpression]:
        """Conversion of field = string value expressions"""
        field = cond.field
        val = cond.value.to_plain()
        val_no_wc = val.rstrip("*").lstrip("*")
        quote = self.get_quote_type(val)
        # contains
        if val.startswith(self.wildcard_single) and val.endswith(self.wildcard_single):
            result = cond.field + self.token_separator + self.icontains_token + self.token_separator + quote + val_no_wc + quote
        # startswith
        elif val.endswith(self.wildcard_single) and not val.startswith(self.wildcard_single):
            result = cond.field + self.token_separator + self.istarts_with_token + self.token_separator + quote + val_no_wc + quote
        # endswith
        elif val.startswith(self.wildcard_single) and not val.endswith(self.wildcard_single):
            escaped_val = re.escape(val_no_wc).replace("/", "\\/") # re.escape is not escaping the forward slash correctly :(
            result = self.re_expression.format(field=field, regex=".*{}$".format(escaped_val))
        # plain equals
        else:
            no_case_str = self.no_case_str_expression.format(value=quote + self.convert_value_str(cond.value, state) + quote)
            result = cond.field + self.token_separator + self.eq_token + self.token_separator + no_case_str

        return result


    def convert_condition_field_eq_val_re(self, cond : ConditionFieldEqualsValueExpression, state : ConversionState) -> Union[str, DeferredQueryExpression]:
        """Conversion of field matches regular expression value expressions."""
        return self.re_expression.format(
            field=cond.field,
            regex=cond.value.regexp
        )


    def convert_icontains_any(self, field, values):
        """Conversion of field contains any in list conditions."""
        result = self.field_icontains_any_expression.format(field=field,
                                                                list=self.list_separator.join([
                                                                    self.get_quote_type(v) + v + self.get_quote_type(v) if isinstance(v, str)
                                                                    else str(v)
                                                                    for v in values
                                                                ]),
                                                            )

        return result


    def convert_icontains_all(self, field, values):
        """Conversion of field contains all in list conditions."""
        result = self.field_icontains_all_expression.format(field=field,
                                                                list=self.list_separator.join([
                                                                    self.get_quote_type(v) + v + self.get_quote_type(v) if isinstance(v, str)
                                                                    else str(v)
                                                                    for v in values
                                                                ]),
                                                            )

        return result


    def convert_istarts_with_any(self, field, values):
        """Conversion of field starts with any in list conditions."""
        result = self.field_istarts_with_any_expression.format(field=field,
                                                                list=self.list_separator.join([
                                                                    self.get_quote_type(v) + v + self.get_quote_type(v) if isinstance(v, str)
                                                                    else str(v)
                                                                    for v in values
                                                                ]),
                                                            )

        return result


    def convert_condition_or(self, cond : ConditionOR, state : ConversionState) -> Union[str, DeferredQueryExpression]:
        """Conversion of OR conditions."""
        # child args all contain values
        if all(["value" in vars(arg).keys() for arg in cond.args]):
            args = cond.args
            mods = [mod for mod in [arg.parent.parent.detection_items[0].modifiers for arg in args]]
            # check whether all args have the same modifiers
            if all(mod == mods[0] for mod in mods):
                vals = [str(arg.value.to_plain() or "") for arg in cond.args]
                vals_no_wc = [val.rstrip("*").lstrip("*") for val in vals]
                fields = list(set([arg.field for arg in cond.args]))
                if len(fields) == 1:    # only one field name across all ORed items.
                    # icontains-any
                    if vals[0].startswith(self.wildcard_single) and vals[0].endswith(self.wildcard_single):
                        result = self.convert_icontains_any(fields[0], vals_no_wc)
                        return result
                    # startswith-any
                    elif vals[0].endswith(self.wildcard_single) and not vals[0].startswith(self.wildcard_single):
                        result = self.convert_istarts_with_any(fields[0], vals_no_wc)
                        return result
                    # endswith-any
                    elif vals[0].startswith(self.wildcard_single) and not vals[0].endswith(self.wildcard_single):
                        field = fields[0]
                        escaped_vals = [re.escape(val).replace("/", "\\/") for val in vals_no_wc]
                        exp = "(.*{}$)".format("$|.*".join(escaped_vals))
                        result = self.re_expression.format(field=field, regex=exp)
                        return result
                    else:
                        return self.field_in_list_expression.format(
                            field=fields[0],
                            list=self.list_separator.join([
                                self.get_quote_type(self.convert_value_str(arg.value, state)) + arg.value.to_plain() + self.get_quote_type(self.convert_value_str(arg.value, state))
                                if isinstance(arg.value, SigmaString)   # string escaping and qouting
                                else str(arg.value)       # value is number
                                for arg in cond.args
                            ]),
                        )
                else:
                    # 'OR' fields differ
                    return self.basic_join_or(cond, state)
            # args have different modifiers
            else:
                return self.basic_join_or(cond, state)
        # child args are other 'OR' or 'AND' expressions
        else:
            return self.basic_join_or(cond, state)


    def convert_condition_and(self, cond : ConditionAND, state : ConversionState) -> Union[str, DeferredQueryExpression]:
        """Conversion of AND conditions."""
        # child args all contain values
        if all(["value" in vars(arg).keys() for arg in cond.args]):
            args = cond.args
            mods = [mod for mod in [arg.parent.parent.detection_items[0].modifiers for arg in args]]
            # check whether all args have the same modifiers
            if all(mod == mods[0] for mod in mods):
                vals = [str(arg.value.to_plain() or "") for arg in cond.args]
                vals = [arg.value.to_plain() or "" for arg in cond.args]
                vals_no_wc = [val.rstrip("*").lstrip("*") for val in vals]
                fields = list(set([arg.field for arg in cond.args]))
                # parent condition has modifiers
                if len(fields) == 1:
                    try:
                        # icontains-all (last condition is SigmaAllModifier or there are two values)
                        if cond.args[0].parent.parent.detection_items[0].modifiers[-1].__name__ == "SigmaAllModifier" or len(vals) == 2:
                            result = self.convert_icontains_all(fields[0], vals_no_wc)
                            return result
                        else:
                            return self.basic_join_and(cond, state)
                    except:
                        return self.basic_join_and(cond, state)
                else:
                    # parent condition does not contain modifiers
                    return self.basic_join_and(cond, state)
            # args have different modifiers
            else:
                return self.basic_join_and(cond, state)
        # child args are other 'OR' or 'AND' expressions
        else:
            return self.basic_join_and(cond, state)

    def finalize_query(self, rule : SigmaRule, query : Union[str, DeferredQueryExpression], index : int, state : ConversionState, output_format : str) -> Union[str, DeferredQueryExpression]:
        """
        Finalize query by appending deferred query parts to the main conversion result as specified
        with deferred_start and deferred_separator.
        """
        # addition of a check for aggregate functions
        agg_function_strings = ["| count", "| min", "| max", "| avg", "| sum"]
        condition_string = " ".join([item.lower() for item in rule.detection.condition])
        if any(f in condition_string for f in agg_function_strings):
            raise SigmaFeatureNotSupportedByBackendError("Aggregate functions are deprecated and are not supported by the InsightIDR backend.", source=rule.detection.condition)

        # finalize
        if state.has_deferred():
            if isinstance(query, DeferredQueryExpression):
                query = self.deferred_only_query
            return super().finalize_query(rule,
                query + self.deferred_start + self.deferred_separator.join((
                    deferred_expression.finalize_expression()
                    for deferred_expression in state.deferred
                    )
                ),
                index, state, output_format
            )
        else:
            return super().finalize_query(rule, query, index, state, output_format)

    # finalize query for use with log search 'Advanced' option
    def finalize_query_leql_advanced_search(self, rule: SigmaRule, query: str, index: int, state: ConversionState) -> str:
        return f"""where({query})"""

    # finalize query the way it appears under Detection Rules -> Attacker Behavior Analytics -> Rule Logic
    def finalize_query_leql_detection_definition(self, rule: SigmaRule, query: str, index: int, state: ConversionState) -> str:
        entry_type = rule.logsource.category
        formatted_query = "\n  ".join(re.split("(AND |OR )", query))
        return f"""from(
  entry_type = {entry_type}"
)
where(
  {formatted_query}
)"""
