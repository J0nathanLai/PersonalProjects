Sample Command Line Code Runs:
To reformat data:
python feature.py \largedata/train_large.tsv \largedata/val_large.tsv \largedata/test_large.tsv \glove_embeddings.txt \largeoutput/formatted_train_large.tsv \largeoutput/formatted_val_large.tsv \largeoutput/formatted_test_large.tsv

To produce output and make predicitons: 
python lr.py \largeoutput/formatted_train_large.tsv \largeoutput/formatted_val_large.tsv \largeoutput/formatted_test_large.tsv \largeoutput/formatted_train_labels.txt \largeoutput/formatted_test_labels.txt \largeoutput/formatted_metrics.txt \500 \0.1
