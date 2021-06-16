from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import IPython
e = IPython.embed

BERT_MODEL = None
BERT_TOKENIZER = None

def bert_embedding(sentence, word, use_gpu=False):
    """return the embedding of the word in the sentence"""
    # since downloading bert is slow: only do it once and cache it as a global variable
    global BERT_MODEL, BERT_TOKENIZER
    if BERT_MODEL is None or BERT_TOKENIZER is None:
        print("one-time downloading of bert")
        BERT_TOKENIZER = BertTokenizer.from_pretrained('bert-base-uncased')
        BERT_MODEL = BertModel.from_pretrained('bert-base-uncased')
        if use_gpu:
            BERT_MODEL = BERT_MODEL.cuda()

    # encode sentence into a list of ids
    input_ids = torch.tensor(BERT_TOKENIZER.encode(sentence)).unsqueeze(0) # TODO Batch size 1, could do more
    if use_gpu:
        input_ids = input_ids.cuda()

    # feed into the model
    with torch.no_grad():
        outputs = BERT_MODEL(input_ids)
    last_hidden_states = outputs[0]  # the hidden-state/embedding we want is the first element of the output tuple
    last_hidden_states = last_hidden_states[0] # TODO Batch size 1, could do more
    last_hidden_states = last_hidden_states.detach().cpu().numpy()

    # figure out what is the index of word in sentence
    tokenized_input = BERT_TOKENIZER.tokenize(sentence)
    assert word in tokenized_input
    index = tokenized_input.index(word) # TODO edge case: multiple appearance
    index += 1 # this is because all inputs are left-pad with one [cls] token

    return last_hidden_states[index]

def test_bert_embedding():
    e1 = bert_embedding("I forgot my key at home.", "forgot", use_gpu=True)
    e2 = bert_embedding("I left my key at home.", "left", use_gpu=True)
    e3 = bert_embedding("She was left behind by her parents.", "left", use_gpu=True)

    e4 = bert_embedding("The entrance is on the left.", "left", use_gpu=True)
    e5 = bert_embedding("The store is on the left hand side.", "left", use_gpu=True)
    e6 = bert_embedding("The entrance is on the right.", "right", use_gpu=True)

    e7 = bert_embedding("I forgot my key at home.", "key", use_gpu=True)
    e8 = bert_embedding("My mom forgot her key at home.", "key", use_gpu=True)
    e9 = bert_embedding("Tony forgot his house's key at home.", "key", use_gpu=True)

    def mean_intra_distance(embeddings):
        all_combinations = []
        for i in range(len(embeddings)):
            for j in range(len(embeddings)-i-1):
                all_combinations.append([i, j+i+1])
        dist = []
        for i, j in all_combinations:
            dist.append(np.linalg.norm(embeddings[i] - embeddings[j]))
        return np.mean(dist)

    # some sanity checks
    print(mean_intra_distance([e1, e2, e3])) # should be small
    print(mean_intra_distance([e4, e5, e6])) # should be small
    print(mean_intra_distance([e7, e8, e9])) # should be very small
    print(mean_intra_distance([e1, e2, e3, e4, e5, e6])) # should be big
    print(mean_intra_distance([e1, e2, e3, e7, e8, e9]))  # should be big


if __name__ == "__main__":
    test_bert_embedding()