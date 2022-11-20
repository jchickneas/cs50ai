import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probDist = dict()

    numPages = len(corpus)
    randProbAllPages = 1/numPages
    weightedProbAllPages = (1-damping_factor)*randProbAllPages

    linkedPages = corpus[page]
    numLinkedPages = len(linkedPages)
    probLinkedPages = 1/numLinkedPages
    weightedProbLinkedPages = damping_factor*probLinkedPages

    pdIter = iter(corpus)
    totalProb = 0
    epsilon=.001

    for pdkey in pdIter:
        #print (corpus[corpkey])
        if pdkey in linkedPages:
            probDist[pdkey] = weightedProbAllPages + weightedProbLinkedPages
        else:
            probDist[pdkey] = weightedProbAllPages
        totalProb += probDist[pdkey]

    if totalProb < 1 - epsilon:
        print ("total probability is " + totalProb + "Probabilities should add up to 1.0!")

   # raise NotImplementedErrorv
    return probDist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    choiceLst = random.choices(list(corpus.keys()))
    page = choiceLst[0]

    estPRVals = dict.fromkeys(iter(corpus), 0)

    for i in range (n):
        pd = transition_model (corpus, page, damping_factor)
        # get new page value using transition model
        choiceLst = random.choices(list(pd.keys()), list(pd.values()))
        page=choiceLst[0]
        estPRVals[page]+=1/n

    return estPRVals

def thresholdMet(convDict, convThreshold):

    cdIter = iter(convDict)

    for cdKey in cdIter:
        if (convDict[cdKey] > convThreshold):
            return False

    return True

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    numKeys=len(corpus)
    # pr due to random surf
    estPRVals = dict.fromkeys(iter(corpus), (1-damping_factor)/numKeys)
    # pr due to link

    convThreshold = .001
    convDict = dict.fromkeys(iter(corpus),2*convThreshold)
    oldEst = dict()
    oldEst.update(estPRVals)
    while (False == thresholdMet (convDict,convThreshold)):
        corpIter = iter(corpus)
        newEst = dict()
        newEst.update(oldEst)
        for corpKey in corpIter:
            oldValue = oldEst[corpKey]
            numLinks = len(corpus[corpKey])
            if (numLinks > 0):
                for linkPage in corpus[corpKey]:
                    newEst[corpKey] += damping_factor*oldEst[linkPage]/numLinks
                convDict[corpKey] = newEst[corpKey]-oldValue
        oldEst.update(newEst)

    return oldEst


if __name__ == "__main__":
    main()
