"""
PageRank Algorithm Implementation

Implement Google's PageRank algorithm to rank web pages
using Markov Models and Random Walks
"""

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
    distribution = {}
    
    # Get all pages in corpus
    all_pages = set(corpus.keys())
    num_pages = len(all_pages)
    
    # Get links from current page
    links = corpus[page]
    num_links = len(links)
    
    # If page has no outgoing links, treat as having links to all pages
    if num_links == 0:
        links = all_pages
        num_links = num_pages
    
    # Calculate probabilities
    for p in all_pages:
        # Base probability (random choice)
        distribution[p] = (1 - damping_factor) / num_pages
        
        # Additional probability if linked from current page
        if p in links:
            distribution[p] += damping_factor / num_links
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    all_pages = list(corpus.keys())
    
    # Initialize all pages with 0 count
    for page in all_pages:
        pagerank[page] = 0
    
    # Start with random page
    current_page = random.choice(all_pages)
    
    # Sample n pages
    for i in range(n):
        # Count current page
        pagerank[current_page] += 1
        
        # Get transition model for current page
        transitions = transition_model(corpus, current_page, damping_factor)
        
        # Choose next page based on probabilities
        pages = list(transitions.keys())
        probabilities = list(transitions.values())
        current_page = random.choices(pages, weights=probabilities)[0]
    
    # Convert counts to probabilities
    for page in pagerank:
        pagerank[page] /= n
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    all_pages = set(corpus.keys())
    num_pages = len(all_pages)
    
    # Initialize all pages with equal probability
    for page in all_pages:
        pagerank[page] = 1 / num_pages
    
    # Create a mapping of which pages link to each page
    incoming_links = {page: set() for page in all_pages}
    for page, links in corpus.items():
        # If page has no outgoing links, it links to all pages
        if not links:
            links = all_pages
        for link in links:
            incoming_links[link].add(page)
    
    # Iteratively update PageRank values
    threshold = 0.001
    while True:
        new_pagerank = {}
        
        for page in all_pages:
            # Start with random surfer probability
            rank = (1 - damping_factor) / num_pages
            
            # Add contributions from pages that link to this page
            for linking_page in incoming_links[page]:
                num_links = len(corpus[linking_page])
                if num_links == 0:
                    num_links = num_pages  # Page links to all pages
                rank += damping_factor * (pagerank[linking_page] / num_links)
            
            new_pagerank[page] = rank
        
        # Check for convergence
        converged = True
        for page in all_pages:
            if abs(new_pagerank[page] - pagerank[page]) > threshold:
                converged = False
                break
        
        pagerank = new_pagerank
        
        if converged:
            break
    
    return pagerank


if __name__ == "__main__":
    main()