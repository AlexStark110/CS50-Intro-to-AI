"""
Heredity - Bayesian Networks and Probability

Calculate probabilities of genetic trait inheritance using Bayesian inference
"""

import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")

    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Everyone else must have no copies of the gene
                have_gene = {
                    person: (
                        2 if person in two_genes else
                        1 if person in one_gene else 0
                    )
                    for person in names
                }

                # Check if current set of people violates known information
                fails_evidence = any(
                    (people[person]["gene"] is not None and
                     people[person]["gene"] != have_gene[person])
                    for person in names
                )
                if fails_evidence:
                    continue

                # Calculate probability for current set of people
                prob = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, prob)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None),
                "gene": (int(row["gene"]) if row["gene"] else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_genes` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set `have_trait` does not have the trait.
    """
    probability = 1.0
    
    # Determine gene count for each person
    gene_count = {}
    for person in people:
        if person in two_genes:
            gene_count[person] = 2
        elif person in one_gene:
            gene_count[person] = 1
        else:
            gene_count[person] = 0
    
    # Calculate probability for each person
    for person in people:
        person_prob = 1.0
        
        # Probability of having this number of genes
        mother = people[person]["mother"]
        father = people[person]["father"]
        
        if mother is None and father is None:
            # No parents in data, use unconditional probability
            person_prob *= PROBS["gene"][gene_count[person]]
        else:
            # Calculate based on parents' genes
            # Probability of inheriting from mother
            mother_genes = gene_count[mother]
            if mother_genes == 2:
                prob_from_mother = 1 - PROBS["mutation"]
            elif mother_genes == 1:
                prob_from_mother = 0.5
            else:
                prob_from_mother = PROBS["mutation"]
            
            # Probability of inheriting from father
            father_genes = gene_count[father]
            if father_genes == 2:
                prob_from_father = 1 - PROBS["mutation"]
            elif father_genes == 1:
                prob_from_father = 0.5
            else:
                prob_from_father = PROBS["mutation"]
            
            # Calculate probability based on gene count
            if gene_count[person] == 2:
                person_prob *= prob_from_mother * prob_from_father
            elif gene_count[person] == 1:
                person_prob *= (prob_from_mother * (1 - prob_from_father) + 
                               (1 - prob_from_mother) * prob_from_father)
            else:
                person_prob *= (1 - prob_from_mother) * (1 - prob_from_father)
        
        # Probability of having trait given gene count
        has_trait = person in have_trait
        person_prob *= PROBS["trait"][gene_count[person]][has_trait]
        
        probability *= person_prob
    
    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Update gene probability
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p
        
        # Update trait probability
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize gene probabilities
        gene_total = sum(probabilities[person]["gene"].values())
        if gene_total > 0:
            for gene_count in probabilities[person]["gene"]:
                probabilities[person]["gene"][gene_count] /= gene_total
        
        # Normalize trait probabilities
        trait_total = sum(probabilities[person]["trait"].values())
        if trait_total > 0:
            for has_trait in probabilities[person]["trait"]:
                probabilities[person]["trait"][has_trait] /= trait_total


if __name__ == "__main__":
    main()