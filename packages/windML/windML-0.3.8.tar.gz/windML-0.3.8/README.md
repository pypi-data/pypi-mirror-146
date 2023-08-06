# WindML

![](images/logo.png)

Refreshingly Lightweight Machine Learning (using only numpy). models include conditional-character-RNN, Transformer and a Direct Feedback Alignment NN and other one-shot models like extreme learning machines or matrix factorisation retrieval-based classifiers (for a model-free alternative). 

## ChangeLog
- 0.3.8 generate function added for RecurrentELM
- 0.3.7 bug fix: RecurrentELM hidden_state initialised in fit
- 0.3.6 ELM sparse weights removed
- 0.3.5 ELM binarisation threshold reduced to improve accuracy
- 0.3.4 ELM binarisation threshold increased slightly to improve efficiency and generalisability
- 0.3.3 ELM stores sparse weights now for generalisability and memory efficiency
- 0.3.2 allow hidden state to be reset
- 0.3.1 kepts recurrent ELM weights random only
- 0.3.0 added recurrent ELM and Autoencoder ELM
- 0.2.3 allow epochs to be specified by user in rnn
- 0.2.2 bug fix. also removing fixed bos, eos, etc tokens and allowing to be set dynamically
- 0.2.1 adding bos, eos, pad token ids and updating epochs
- 0.2.0 token-level rnn added
- 0.1.3 bug fix: adding init file
- 0.1.2 char-rnn can now take context vector for conditional generation
- 0.1.1 refactor char-rnn code
- 0.1.0 added char-rnn model
- 0.0.2 bug fix: adding init files to directories
- 0.0.1 initial release