#!/bin/bash

FILTERED_EMBEDDING=../data/glove.840B.300d.txt.filtered
if [ -f "$FILTERED_EMBEDDING" ]; then
  echo "$FILTERED_EMBEDDING found in data directory"
else
  echo "$FILTERED_EMBEDDING not found, downloading..."
  curl -O http://downloads.cs.stanford.edu/nlp/data/glove.840B.300d.zip
  unzip glove.840B.300d.zip
  rm glove.840B.300d.zip
fi

E2E_EMBEDDING=../data/e2e_pretrained_glove_embeddings.txt
if [ -f "$E2E_EMBEDDING" ]; then
 echo "$E2E_EMBEDDING found in data directory"
else
  echo "$E2E_EMBEDDING not found, downloading..."
  echo "Accessing official google drive link from repository: https://github.com/kentonl/e2e-coref"

  # instructions:
  # https://medium.com/@acpanjan/download-google-drive-files-using-wget-3c2c025a8b99  

  FILE_ID=1fkifqZzdzsOEo0DXMzCFjiNXqsKG_cHi
  wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1fkifqZzdzsOEo0DXMzCFjiNXqsKG_cHi' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1fkifqZzdzsOEo0DXMzCFjiNXqsKG_cHiD" -O e2e_glove_embedding && rm -rf /tmp/cookies.txt
  tar -xf e2e-coref.tgz
fi

python filter_embeddings.py glove.840B.300d.txt