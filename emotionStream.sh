#!/usr/bin/env bash


java -Xmx2000m -cp EmotionTagger/release/lib/emotiontagger-v1.0-jar-with-dependencies.jar TagTextStreamWithEmotionsAndExpression --emotion-lexicon "EmotionTagger/release/resources/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt" --intensifiers "EmotionTagger/release/resources/intensifiers.txt"  --intensifiers "EmotionTagger/release/resources/weakeners.txt"
