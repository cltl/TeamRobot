#!/usr/bin/env bash


java -Xmx2000m -cp EmotionTagger/release/lib/emotiontagger-v1.0-jar-with-dependencies.jar TagTextStreamWithEmotionsAndExpression --emotion-lexicon "resources/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt" --intensifiers "resources/intensifiers.txt"  --intensifiers "resources/weakeners.txt"
