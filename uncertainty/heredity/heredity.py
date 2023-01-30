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

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

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
                          False if row["trait"] == "0" else None)
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


def get_no_genes (people, one_gene, two_genes):
    # get all people remove one and two genes
    allPeeps = people.keys()

    remPeeps = allPeeps - one_gene
    remPeeps = remPeeps - two_genes
    return remPeeps

def get_doesnt_have_trait (people, has_trait):
    # get all people remove one and two genes
    allPeeps = people.keys()

    remPeeps = allPeeps - has_trait
    return remPeeps

def prob_no_genes(no_genes):

    raise NotImplementedError

def prob_one_gene(one_genes):


    raise NotImplementedError

def prob_two_genes(two_genes):

    raise NotImplementedError

def prob_has_trait(has_trait):

    raise NotImplementedError


def prob_doesnt_have_trait(doesnt_have_trait):

    raise NotImplementedError

def joint_probability(people, one_gene, two_genes, have_trait):

    probability = dict()

    no_genes = get_no_genes(people, one_gene, two_genes)

    doesnt_have_trait=get_doesnt_have_trait(people, have_trait)

    p0g = prob_no_genes(no_genes)

    p1g = prob_one_gene(one_gene)

    p2g = prob_two_genes(two_genes)

    pht = prob_has_trait(have_trait)

    pnt = prob_doesnt_have_trait(doesnt_have_trait)
# TODO
    #probability = dict("genes"=p0g, )

    """
    Compute and return a joint probability.


    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    return probability



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
#    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # raise NotImplementedError
    # check
    sum1 = probabilities["gene"][0] + probabilities["gene"][1] + probabilities["gene"][2]
    if sum1 != 1.0:
        ratio = 1/sum1
        #scale each value by ratio
        probabilities["gene"][0]*=ratio
        probabilities["gene"][1]*=ratio
        probabilities["gene"][2]*=ratio

    sum2 = probabilities["trait"][0][True] + probabilities["trait"][0][False]

    if sum2 != 1.0:
        ratio2 = 1/sum2
        #scale each value by ratio
        probabilities["trait"][0][True]*=ratio2
        probabilities["trait"][0][False]*=ratio2

if __name__ == "__main__":
    main()
