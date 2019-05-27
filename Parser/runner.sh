#!/usr/bin/env bash

# Go to directory containing CoreNLP data and start the server.
java -mx5g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 8080 -port 8080 -timeout 30000000
