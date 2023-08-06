"""Gapfilling functions. Mostly a meneco interface."""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Dict, Iterable, Set, Tuple, cast

from clyngor.as_pyasp import Term, TermSet
from meneco.meneco import query

if TYPE_CHECKING:
    from ..core.model import Model

__all__ = ["gapfilling"]


def model_to_termset(model: "Model", model_name: str) -> TermSet:
    model_terms = []
    for reaction in model.reactions.values():
        model_terms.append(Term("reaction", [f'"{reaction.id}"', f'"{model_name}"']))
        substrates, products = reaction.split_stoichiometries()
        for substrate in substrates:
            model_terms.append(
                Term(
                    "reactant",
                    [
                        f'"{substrate}"',
                        f'"{reaction.id}"',
                        f'"{model_name}"',
                    ],
                )
            )
        for product in products:
            model_terms.append(
                Term(
                    "product",
                    [
                        f'"{product}"',
                        f'"{reaction.id}"',
                        f'"{model_name}"',
                    ],
                )
            )
    return TermSet(model_terms)


def name_to_term(compound_type: str, compound_id: str) -> Term:
    return Term(compound_type, [f'"{compound_id}"'])


def names_to_termset(compound_type: str, compound_iterable: Iterable[str]) -> TermSet:
    terms = []
    for compound_id in compound_iterable:
        terms.append(name_to_term(compound_type, compound_id))
    return TermSet(terms)


def get_unproducible(model: TermSet, target: TermSet, seed: TermSet) -> set[str]:
    return set(
        i[0] for i in cast(dict, query.get_unproducible(model, target, seed)).get("unproducible_target", [])
    )


def get_intersection_of_completions(
    draft: TermSet, repairnet: TermSet, seeds: TermSet, targets: TermSet
) -> set[str]:
    intersection = cast(
        Dict[str, Set[Tuple[str, str]]],
        query.get_intersection_of_completions(
            draft=draft,
            repairnet=repairnet,
            seeds=seeds,
            targets=targets,
        ),
    )
    rxns = intersection.get("xreaction")
    if rxns is None:
        return set()
    return set(i[0] for i in rxns)


def gapfilling(
    model: "Model",
    db: "Model",
    seed: Iterable[str],
    targets: Iterable[str],
    include_weak_cofactors: bool = False,
) -> set[str]:
    seed = set(seed)
    if include_weak_cofactors:
        seed = seed.union(set(db.get_weak_cofactor_duplications()))

    for target in targets:
        if target not in db.compounds:
            warnings.warn(f"Target '{target}' could not be found in the database")

    model_termset = model_to_termset(model, "draft")
    db_termset = model_to_termset(db, "repair")
    seed_termset = names_to_termset("seed", seed)
    target_termset = names_to_termset("target", targets)

    return get_intersection_of_completions(
        draft=model_termset,
        repairnet=db_termset,
        seeds=seed_termset,
        targets=target_termset,
    ).difference(model.reactions)
