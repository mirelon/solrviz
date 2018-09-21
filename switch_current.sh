touch docs/$1.csv freqs/$1.csv avgwls/$1
ln -sf docs/$1.csv current_docs
ln -sf freqs/$1.csv current_freqs
ln -sf avgwls/$1 current_avgwls
