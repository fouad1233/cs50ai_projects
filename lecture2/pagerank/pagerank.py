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
    probability_dis = {}
    all_pages_num = len(corpus)
    linked_pages_num = len(corpus[page])
    
    if linked_pages_num < 1:
        for key in corpus:
            probability_dis[key] = 1 / all_pages_num # all pages have equal probability
    else:
        random_factor_prob = (1 - damping_factor) / all_pages_num
        linked_factor_prob = damping_factor / linked_pages_num
        for key in corpus:
            if key in corpus[page]:
                probability_dis[key]  = linked_factor_prob + random_factor_prob
            else:
                probability_dis[key] = random_factor_prob
            
    return probability_dis


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start_page = random.choice(list(corpus.keys()))
    
    page_rank = {}
    for key in corpus:
        page_rank[key] = 0
    
    for i in range(n):
        page_rank[start_page] += 1
        prob_dis = transition_model(corpus, start_page, damping_factor)
        start_page = random.choices(list(prob_dis.keys()), weights=list(prob_dis.values()))[0]
    
    for key in page_rank:
        page_rank[key] /= n
    
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    init_page_rank = {}
    page_num = len(corpus)
    for page in corpus:
        init_page_rank[page] = 1 / page_num
        
    new_page_rank = {}
    
    while True:
        for page in corpus:
            val = 0
            for link in corpus:
                if page in corpus[link]:
                    val+= ( init_page_rank[link] / len(corpus[link]))
                if len(corpus[link]) == 0:
                    val += (init_page_rank[link] / page_num) 
            val *= damping_factor
            val += (1 - damping_factor) / page_num
            
            new_page_rank[page] = val
        

        diff = max([abs(new_page_rank[page] - init_page_rank[page]) for page in init_page_rank  ])
        if diff < 0.001:
            break
        else:
            init_page_rank = new_page_rank.copy()
        
    return init_page_rank
    


if __name__ == "__main__":
    main()
