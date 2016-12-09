#SESaR
##Semantic-, Emotional-, Structure Processor & Response Generator  
######A demo of a linguistic processor, built for the VPRO Robot project

The simplest way to get the demo running at the moment is to first install the SpaCy python package (pip install spacy or however you install your packages). Then download the SpaCy language models:  (see also [https://spacy.io/docs/usage/](https://spacy.io/docs/usage/)

You can run the conversation.py script by invoking 'python conversation.py' from your command line. It will take a little while to load, but after that you can type in text and the computer will return something (at the moment this is just the output from the named entity recognition module, over the weekend this will be integrated with the sesar.py and response_module.py to perform the other processing steps).
