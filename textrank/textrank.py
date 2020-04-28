import argparse
from data import build_vocabulary
from data import filter_sentences
from data import load_data
from model import build_coo_matrix
from model import build_similarity_matrix
from model import get_topk_keywords
from model import get_topk_sentences
from model import pagerank
import os
import sys

def extract_keywords(sentences, k=5):
    filtered_sentences = filter_sentences(sentences, lowercase=False, stem=False)

    word_to_ix, ix_to_word = build_vocabulary(filtered_sentences)

    S = build_coo_matrix(filtered_sentences, word_to_ix)

    ranks = pagerank(S)

    return get_topk_keywords(ranks, ix_to_word, k)

def summarize(sentences, k=5):
    filtered_sentences = filter_sentences(sentences)

    S = build_similarity_matrix(filtered_sentences)

    ranks = pagerank(S)

    return get_topk_sentences(ranks, sentences, k)

def gettxt(filename):
    # os.makedirs(filename)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path to text file")
    parser.add_argument("-s", "--summarize", action="store_true",
        help="Summarize text, otherwise extract keywords")
    parser.add_argument("-l", "--len", type=int,
        help="Number of keywords/sentences to extract")
    parser.add_argument("-t", "--output", help="Path to output text file")
 

    args = parser.parse_args()

    k = 5
    
    x =filename+'.txt'
    f = open(x,'w+')
    if args.len:
        k = args.len

    sentences = load_data(args.path)
    
    if args.summarize:
        summary = summarize(sentences, k)
        # print(" ".join(summary))
        print(" ".join(summary),file = f)
        return
        # print("; ".join(extract_keywords(sentences, k)))
    print("; ".join(extract_keywords(sentences, k)), file = f)
    f.close()

if __name__ == '__main__':

    filename = sys.argv[-1]
    gettxt(filename)
   
