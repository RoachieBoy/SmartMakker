# GPT-like model-arguments analysis

- [GPT-like model-arguments analysis](#gpt-like-model-arguments-analysis)
  - [Forward](#forward)
    - [input\_ids](#input_ids)
    - [past\_key\_values](#past_key_values)
    - [attention\_mask](#attention_mask)
    - [token\_type\_ids](#token_type_ids)
    - [position\_ids](#position_ids)
    - [head\_mask](#head_mask)
    - [inputs\_embeds](#inputs_embeds)
    - [use\_cache](#use_cache)
    - [output\_attentions](#output_attentions)
    - [output\_hidden\_states](#output_hidden_states)
    - [return\_dict](#return_dict)
    - [labels](#labels)
  - [Forward Output](#forward-output)
    - [loss](#loss)
    - [logits](#logits)
    - [hidden\_states](#hidden_states)
    - [attentions](#attentions)
    - [cross\_attentions](#cross_attentions)
    - [past\_key\_values](#past_key_values-1)
  - [Tokenization](#tokenization)
    - [vocab\_file (str)](#vocab_file-str)
    - [merges\_file (str)](#merges_file-str)
    - [errors](#errors)
    - [unk\_token](#unk_token)
    - [bos\_token](#bos_token)
    - [eos\_token](#eos_token)
    - [add\_prefix\_space](#add_prefix_space)
  - [GPT-2 LM Head Model](#gpt-2-lm-head-model)
    - [Config](#config)
      - [vocab\_size](#vocab_size)
      - [n\_positions](#n_positions)
      - [n\_embd](#n_embd)
      - [n\_layer](#n_layer)
      - [n\_head](#n_head)
      - [n\_inner](#n_inner)
      - [activation\_function](#activation_function)
      - [resid\_pdrop](#resid_pdrop)
      - [embd\_pdrop](#embd_pdrop)
      - [attn\_pdrop](#attn_pdrop)
      - [layer\_norm\_epsilon](#layer_norm_epsilon)
      - [initializer\_range](#initializer_range)
      - [summary\_type](#summary_type)
      - [summary\_use\_proj](#summary_use_proj)
      - [summary\_activation](#summary_activation)
      - [summary\_proj\_to\_labels](#summary_proj_to_labels)
      - [summary\_first\_dropout](#summary_first_dropout)
      - [scale\_attn\_weights](#scale_attn_weights)
      - [use\_cache](#use_cache-1)
      - [scale\_attn\_by\_inverse\_layer\_idx](#scale_attn_by_inverse_layer_idx)
      - [reorder\_and\_upcast\_attn](#reorder_and_upcast_attn)
  - [GPTNeoForCasualLM](#gptneoforcasuallm)
    - [Config](#config-1)
      - [vocab\_size](#vocab_size-1)
      - [attention\_types](#attention_types)
      - [hidden\_size](#hidden_size)
      - [num\_layers](#num_layers)
      - [num\_heads](#num_heads)
      - [intermediate\_size](#intermediate_size)
      - [activation\_function](#activation_function-1)
      - [embed\_dropout](#embed_dropout)
      - [attention\_dropout](#attention_dropout)
      - [max\_position\_embeddings](#max_position_embeddings)
      - [type\_vocab\_size](#type_vocab_size)
      - [initializer\_range](#initializer_range-1)
      - [layer\_norm\_epsilon](#layer_norm_epsilon-1)
      - [use\_cache](#use_cache-2)

## Forward 

The forward method of both models has the following parameters:

### input_ids

Indices of input sequence tokens in the vocabulary.

> If past_key_values is used, only input_ids that do not have their past calculated should be passed as input_ids.

### past_key_values

Contains precomputed hidden-states (key and values in the attention blocks) as computed by the model (see past_key_values output below). 

> Can be used to speed up sequential decoding. 

The input_ids which have their past given to this model should not be passed as input_ids as they have already been computed.

### attention_mask 

Mask to avoid performing attention on padding token indices. Mask values selected in [0, 1]:

- 1 for tokens that are not masked,
- 0 for tokens that are masked.

> If past_key_values is used, attention_mask needs to contain the masking strategy that was used for past_key_values. In other words, the attention_mask always has to have the length: len(past_key_values) + len(input_ids)

### token_type_ids 
Segment token indices to indicate first and second portions of the inputs. Indices are selected in [0, 1]:

- 0 corresponds to a sentence A token,
- 1 corresponds to a sentence B token.

### position_ids 
Indices of positions of each input sequence tokens in the position embeddings. 

> Selected in the range [0, config.max_position_embeddings - 1].

### head_mask 
Mask to nullify selected heads of the self-attention modules. Mask values selected in [0, 1]:

- 1 indicates the head is not masked,
- 0 indicates the head is masked.

### inputs_embeds
Optionally, instead of passing input_ids you can choose to directly pass an embedded representation. This is useful if you want more control over how to convert input_ids indices into associated vectors than the model’s internal embedding lookup matrix.

> If past_key_values is used, optionally only the last inputs_embeds have to be input (see past_key_values).

### use_cache 

If set to True, past_key_values key value states are returned and can be used to speed up decoding (see past_key_values).

### output_attentions 

Whether or not to return the attentions tensors of all attention layers. See attentions under returned tensors for more detail.

### output_hidden_states 

Whether or not to return the hidden states of all layers. See hidden_states under returned tensors for more detail.

### return_dict 

Whether or not to return a ModelOutput instead of a plain tuple.

### labels 

Labels for language modeling. 

> Note that the labels are shifted inside the model, i.e. you can set labels = input_ids Indices are selected in [-100, 0, ..., config.vocab_size] All labels set to -100 are ignored (masked), the loss is only computed for labels in [0, ..., config.vocab_size]

## Forward Output

### loss

Language modeling loss (for next-token prediction).

### logits

Prediction scores of the language modeling head (scores for each vocabulary token before SoftMax).

### hidden_states

Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.

### attentions

Attentions weights after the attention softmax, used to compute the weighted average in the self-attention heads.

### cross_attentions 

Cross attentions weights after the attention softmax, used to compute the weighted average in the cross-attention heads.

### past_key_values 

Contains pre-computed hidden-states (key and values in the attention blocks) that can be used (see past_key_values input) to speed up sequential decoding.

## Tokenization

Tokenization is done using the GPT2Tokenizer for both GPT-2 and GPT-Neo. The GPT2Tokenizer is a tokenizer that is used to convert a string in a sequence of tokens (string -> tokens). It is based on Byte-Pair-Encoding (BPE) and contains a set of rules to encode a string as a list of tokens.

### vocab_file (str)

Path to the vocabulary file.

### merges_file (str) 

Path to the merges file.

### errors 

Paradigm to follow when decoding bytes to UTF-8.

### unk_token 

The unknown token. A token that is not in the vocabulary cannot be converted to an ID and is set to be this token instead.

### bos_token 

The beginning of sequence token.

### eos_token

The end of sequence token.

### add_prefix_space 

Whether or not to add an initial space to the input. 

> This allows to treat the leading word just as any other word. (GPT2 tokenizer detect beginning of words by the preceding space).

## GPT-2 LM Head Model

GPT2LMHeadModel is a language model developed by OpenAI that is capable of generating natural language text. It is a variant of the GPT-2 model that has been fine-tuned specifically for language generation tasks, such as writing coherent and grammatically correct sentences or paragraphs. 

### Config

#### vocab_size 

Defines the number of different tokens that can be represented by the inputs_ids passed when calling the forward method of the GPT2Model.

#### n_positions 

The maximum sequence length that this model might ever be used with. 

> Typically, set this to something large just in case (e.g., 512 or 1024 or 2048).

#### n_embd 

Dimensionality of the embeddings and hidden states.

#### n_layer 

Number of hidden layers in the Transformer encoder.

#### n_head 

Number of attention heads for each attention layer in the Transformer encoder.

#### n_inner 

Dimensionality of the inner feed-forward layers. 

> None will set it to 4 times n_embd


#### activation_function 

Activation function, to be selected in the list ["relu", "silu", "gelu", "tanh", "gelu_new"].

#### resid_pdrop 

The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.

#### embd_pdrop 

The dropout ratio for the embeddings.

#### attn_pdrop 

The dropout ratio for the attention.

#### layer_norm_epsilon 

The epsilon to use in the layer normalization layers.

#### initializer_range 

The standard deviation of the truncated_normal_initializer for initializing all weight matrices.

#### summary_type 

Has to be one of the following options:

- "last": Take the last token hidden state (like XLNet).
- "first": Take the first token hidden state (like BERT).
- "mean": Take the mean of all tokens hidden states.
- "cls_index": Supply a Tensor of classification token position (like GPT/GPT-2).
- "attn": Not implemented now, use multi-head attention.

#### summary_use_proj 

Whether or not to add a projection after the vector extraction.

#### summary_activation 

Pass "tanh" for a tanh activation to the output, any other value will result in no activation.

#### summary_proj_to_labels 

Whether the projection outputs should have config.num_labels or config.hidden_size classes.

#### summary_first_dropout 

The dropout ratio to be used after the projection and activation.

#### scale_attn_weights 

Scale attention weights by dividing by sqrt(hidden_size).

#### use_cache 

Whether or not the model should return the last key/values attentions (not used by all models).

#### scale_attn_by_inverse_layer_idx 

Whether to additionally scale attention weights by 

```math
1 / layer\_idx + 1
```

#### reorder_and_upcast_attn 

Whether to scale keys (K) prior to computing attention (dot-product) and upcast attention dot-product/softmax to float() when training with mixed precision.

## GPTNeoForCasualLM

GPTNeoForCausalLM is a language model developed by EleutherAI that specializes in generating coherent and contextually-appropriate text. It is built on the GPT-Neo architecture and trained on a large corpus of text using unsupervised learning.

### Config

#### vocab_size 

Defines the number of different tokens that can be represented by the inputs_ids passed to the forward method of GPTNeoModel.

#### attention_types 

The type of attention for each layer in a List of the following format [[["attention_type"], num_layerss]]

> e.g. for a 24 layer model [[["global"], 24]] or [[["global", "local"], 12]] 

Choose the value of attention_type from ["global", "local"]

#### hidden_size 

Dimensionality of the encoder layers and the pooler layer.

#### num_layers

Number of hidden layers in the Transformer encoder.

#### num_heads

Number of attention heads for each attention layer in the Transformer encoder.

#### intermediate_size

Dimensionality of the “intermediate” (i.e., feed-forward) layer in the Transformer encoder.

#### activation_function 

The non-linear activation function (function or string) in the encoder and pooler. 

> If string, "gelu", "relu", "selu" and "gelu_new" are supported.

#### embed_dropout 

The dropout probabilitiy for all fully connected layers in the embeddings, encoder, and pooler.

#### attention_dropout 

The dropout ratio for the attention probabilities.

#### max_position_embeddings 

The maximum sequence length that this model might ever be used with. 

> Typically set this to something large just in case (e.g., 512 or 1024 or 2048).

#### type_vocab_size 

The vocabulary size of the token_type_ids passed when calling GPTNeoModel.

#### initializer_range

The standard deviation of the truncated_normal_initializer for initializing all weight matrices.

#### layer_norm_epsilon 

The epsilon used by the layer normalization layers.

#### use_cache 

Whether or not the model should return the last key/values attentions (not used by all models). 

> Only relevant if config.is_decoder=True.
