import ast
from collections.abc import Iterable
from typing import Type, TypeVar, Tuple

__all__ = [
    'nodes_of_class',
    'is_compliment',
    'compliment_bools',
    'assign_types',
    'assigning_to_same_target',
    'get_assign_target',
    'dirty_compare',
    'match_ends',
]

T = TypeVar('T')
type_t = Type[T] | Tuple[Type[T], ...]

assign_types = (ast.Assign, ast.AnnAssign, ast.AugAssign)
_compliment_operators = {
    ast.Eq: ast.NotEq,
    ast.Lt: ast.GtE,
    ast.LtE: ast.Gt,
    ast.Is: ast.IsNot,
    ast.In: ast.NotIn,
}
_compliment_operators |= {v: k for k, v in _compliment_operators.items()}


def nodes_of_class(node: ast.AST, cls: type_t) -> Iterable[T]:
    for child in ast.walk(node):
        if isinstance(child, cls):
            yield child


def are_compliment_operators(n1, n2):
    return type(n1) == _compliment_operators[type(n2)]


def dirty_compare(n1: ast.AST | Iterable[ast.AST],
                  n2: ast.AST | Iterable[ast.AST]):
    if isinstance(n1, Iterable) and isinstance(n2, Iterable):
        n1, n2 = list(n1), list(n2)
        return (
                len(n1) == len(n2)
                and all(dirty_compare(n1, n2)
                        for n1, n2 in zip(n1, n2))
        )
    return (
            isinstance(n1, ast.AST)
            and isinstance(n2, ast.AST)
            and ast.dump(n1) == ast.dump(n2)
    )


def are_compliment_binary_expressions(n1, n2):
    """Matches `x < 5` compliments `x >= 5 `"""
    match (n1, n2):
        case (
            ast.Compare(left=l1, comparators=c1, ops=[o1]),
            ast.Compare(left=l2, comparators=c2, ops=[o2]),
        ) if (
                dirty_compare(l1, l2)
                and dirty_compare(c1, c2)
                and are_compliment_operators(o1, o2)
        ):
            return True
    return False


def are_complimentary_unary_expressions(n1, n2):
    """matches `x` compliments `not x`"""
    match (n1, n2):
        case (
            cond1,
            ast.UnaryOp(op=ast.Not(), operand=cond2),
        ) if dirty_compare(cond1, cond2):
            return True
    return False


def are_complimented_expression_boolean_literals(n1, n2):
    """
    matches `x < 5 == True` compliments `x < 5 == False`
    """
    match (n1, n2):
        case (
            ast.Compare(left=l1,
                        comparators=[*r1, ast.Constant(value=v1)],
                        ops=[*_, o1]),
            ast.Compare(left=l2,
                        comparators=[*r2, ast.Constant(value=v2)],
                        ops=[*_, o2]),
        ) if (
                dirty_compare(l1, l2)
                and dirty_compare(r1, r2)
                and compliment_bools(v1, v2)
                and dirty_compare(o1, o2)
        ):
            return True


def is_compliment(n1, n2):
    return (
            are_compliment_binary_expressions(n1, n2)
            or are_complimentary_unary_expressions(n1, n2)
            or are_complimented_expression_boolean_literals(n1, n2)
    )


def get_assign_target(n):
    if isinstance(n, ast.Assign):
        return n.targets
    if isinstance(n, ast.AnnAssign):
        return [n.target]
    if isinstance(n, ast.AugAssign):
        return [n.target]


def assigning_to_same_target(n1, n2):
    t1 = get_assign_target(n1)
    t2 = get_assign_target(n2)
    return dirty_compare(t1, t2)


def compliment_bools(v1, v2):
    return isinstance(v1, bool) and isinstance(v2, bool) and v1 != v2


def match_ends(nodes1, nodes2):
    matching = 0
    for n1, n2 in zip(reversed(nodes1), reversed(nodes2)):
        if dirty_compare(n1, n2):
            matching += 1
        else:
            break
    return matching
