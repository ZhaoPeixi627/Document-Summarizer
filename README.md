# Document-Summarizer
## Project Discription
Product Mission: The mission of this product is to be able to summarize and extract keywords of an input txt or pdf file by users. Through some NLP algorithm, we output a shorter txt file with the important information of the input file.
## MVP
The product will at a minimum be able to summarize the user's input txt file and output the main information of the file as a txt file. If time permits, we will build a uers' interface on a website that user can input their file on website and get the result through our website. Also if time permits, we will realize translation of the input file. For example if your input file is a txt file which using Chinese words or other languagues, we can also able to summarize the main idea of the input file.
## User Stories
* I, a student, want to get a summary idea of paper instead of reading it from top to bottom.
* I, a busy white collar, want to have a total idea of news without wasting time on details.
## Initial Plan of Attack
* Have each person in the team select different NLP api or algorithm.
* Compare different NLP api or algorithm and find the best to use for our product.
* After selecting the NLP api or algorithm, we build out back end for our product.
* Finally build our front end(users' interface).
## System Architecture
### Back end
<div align=center><img src="https://github.com/ZhaoPeixi627/Document-Summarizer/blob/master/structure.jpg"/></div>  

## Algorithm  
Textrank is an algorithm orginated from Pagerank, designed by Google in 1997. The main idea of Pagerank is:  
* Important pages are linked by important pages.
* The PageRank value of a page is the probability of a user visiting that page.  
In TextRank, the only difference is that we consider sentences instead of pages.
### Textrank for keywords extraction
* First seperate the text file into sentences.
* For each sentence, apply tokenization, Part-of-Speech tagging and filtering. Detect the important words like noun, verb, and adjective and delete the unimportant words.
* Then create a keyword graph G=(V,E). The nodes represents the keywords, and then use co-occurence to create edges between nodes.
* Apply the textrank formula to get weighted graph, sort the keywords by weight and get a certain number of top-ranked keywrods.  
### Textrank for summarization
* The first step would be to concatenate all the text contained in the articles and split the text into individual sentences.
* In the next step, we will find vector representation (word embeddings) for each and every sentence.
* Similarities between sentence vectors are then calculated and stored in a matrix.
* The similarity matrix is then converted into a graph, with sentences as vertices and similarity scores as edges, for sentence rank calculation.
* Finally, a certain number of top-ranked sentences form the final summary.
## Preparation
* Install NLTK http://www.nltk.org/install.html
* Install NLTK data https://www.nltk.org/data.html
## Implementation  
The python implementation we used is from Bringing Order into Texts (Mihalcea and Tarau, 2004). The paper proposed two unsupervised methods to extract keywords and summarize document, respectively.
* It uses undirected graph to extract keywords and similarity matrix for summarization.
* Python NLTK package is a very advanced NLP tool, here it's used for Tokenization, which can seperate words from sentences.
* NLTK's built-in stopwords list is used to remove unimportant words.
* Part-of-Speech Tagging is also employed to detect nouns and adjectives.  
With this implementation, we can extract a setting number of keywords from document summarize it in a setting number of sentences.
## Examples
We use a piece of Coronavirus news as an example, named input.txt:
> Centers for Disease Control and Prevention Director Dr. Robert Redfield issued new guidelines for essential workers who have been exposed to the coronavirus, saying individuals would need to be asymptomatic to return to work. The guidelines, he said, are aimed at keeping essential workers, including first responders, health care workers, employees in the food supply chain and others at work -- even if they might have been exposed to someone who has coronavirus. “These are individuals that have been within six feet of a confirmed case or a suspected case so that they can, under certain circumstances, they can go back to work if they are asymptomatic,” Redfield said. Redfield said those individuals could return to their jobs if they take their temperature before work, wear a face mask at all times and practice social distancing at work. He reiterated that people should stay home if they feel sick, should not share items used on or near their face and should refrain from congregating in break rooms and other crowded places. The CDC’s new guidelines also outlined steps employers should take, including checking temperatures before employees start work, sending anyone who becomes sick home and cleaning commonly touched surfaces more frequently, among others.  

If the generated file is named newfile.txt
* Extract 10 keywords from the news:  
```python textrank.py -p input.txt -l 10 -t newfile```
<div align=center><img src="https://github.com/ZhaoPeixi627/Document-Summarizer/blob/master/test_extract.png"/></div>

* Summarize the news in 3 sentences  
```python textrank.py -p input.txt -s -l 3 -t newfile```
<div align=center><img src="https://github.com/ZhaoPeixi627/Document-Summarizer/blob/master/text_sum.png"/></div>  

## Front end
A website that can upload file and download generated file.  
We create a web interface with using python flask and we uploaded it to an ec2 instance.  
<div align = center><img src="https://github.com/ZhaoPeixi627/Document-Summarizer/blob/master/interface.png"/></div>  
With this interface, we can accomplish upload text file, process file and download summarized file.  
We also upload our project to ec2 instance.
Website:
"http://ec2-3-132-213-15.us-east-2.compute.amazonaws.com:5000/".

## References
* https://github.com/acatovic/textrank
* R. Mihalcea and P. Tarau. 2004. TextRank: Bringing Order into Texts.
* D. Greene and P. Cunningham. 2006. Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering. In Proc. 23rd International Conference on Machine learning (ICML'06). ACM Press.
* S. Brin and L. Page. 1998. The anatomy of large-scale hyper-textual Web search engine. Computer Networks and ISDN Systems, 30(1-7)
