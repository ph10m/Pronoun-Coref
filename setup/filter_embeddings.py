# coding=utf-8
import sys
import json
import os
import argparse

data_path = "../data"
embedding_dir = "../../../../embeddings"

def get_jsonlines(filename):
  return os.path.join(data_path, "{}.jsonlines".format(filename))

def get_embedding(filename):
  return os.path.join(embedding_dir, filename)

def verify_embedding(embedding):
  if embedding not in os.listdir(embedding_dir):
    print("missing embedding, check the directory for embeddings")
  
  emb_file = get_embedding(embedding)
  print("GloVe embedding {} with size {} MB".format(
    embedding, os.stat(emb_file).st_size // 10**6
  ))
  
  return emb_file

# the pretrained GloVe embeddings by (glove_50_300d_2.txt)
# https://github.com/kentonl/e2e-coref
# https://arxiv.org/abs/1804.05392
E2E_EMBEDDING = "e2e_pretrained_glove_embeddings.txt"

def main(args):
  embedding = verify_embedding(args.embedding)

  words_to_keep = set()

  train = get_jsonlines("train")
  test = get_jsonlines("test")
  dev = get_jsonlines("dev")
  
  files = [train, test, dev]

  for _file in files:
    with open(_file, encoding="utf8") as json_file:
      for line in json_file.readlines():
        for sentence in json.loads(line)["sentences"]:
          words_to_keep.update(sentence)

  print("Found {} words in {} dataset(s)".format(len(words_to_keep), len(files)))

  total_lines = 0
  kept_lines = 0

  # the filtered file to keep for later use
  # store this one in the local data folder
  out_filename = os.path.join(data_path, "{}.filtered".format(args.embedding))

  # open the originally passed glove embedding
  # write to the new filtered file
  with open(embedding, encoding="utf8") as in_file:
    with open(out_filename, "w", encoding="utf8") as filtered:
      for line in in_file.readlines():
        total_lines += 1
        word = line.split()[0]
        if word in words_to_keep:
          kept_lines += 1
          filtered.write(line)

  print("Kept {} out of {} lines.".format(kept_lines, total_lines))
  print("Wrote result to {}.".format(out_filename))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--embedding",
                      required=False,
                      default="glove.6B.300d.txt",
                      help="The GloVe embedding file to use, e.g. glove.6B.300d.txt"
  )

  main(parser.parse_args())