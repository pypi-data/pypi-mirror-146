**sarscov2vec** is an application of continuous vector space representation on novel species of coronaviruses genomes as the methodology of genome feature extraction step, to distinguish the most common 5 different SARS-CoV-2 variants (Alpha, Beta, Delta, Gamma, Omicron) by supervised machine learning model.  
  
In this research we used **367,004 unique and complete genome sequence** records from the official virus repositories. Prepared datasets for this research had balanced classes. Sub-set of 25,000 sequences from the final dataset were randomly selected and used to train the Natural Language Processing (NLP) algorithm. The next 36,365 of samples, unseen by embedding training sessions, were processed by machine learning pipeline. Each SARS-CoV-2 variant was represented by 12,000 samples from different parts of the world. Data separation between embedding and classifier was crucial to prevent the data leakage, which is a common problem in NLP.

Our research results show that the final hiper-tuned machine learning model achieved **99% of accuracy on the test set**. Furthermore, this study demonstrated that the continuous vector space representation of SARS-CoV-2 genomes can be decomposed into 2D vector space and visualized as a method of explanation machine learning model decision.

The proposed methodology wrapped in the _sarscov2vec_ brings a new alignment-free AI-aided bioinformatics tool that distinguishes different SARS-CoV-2 variants solely on the genome sequences. Importantly, the obtained results serve as the proof of concept that the presented approach can also be applied in understanding the genomic diversity of other pathogens.
  

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/sarscov2vec.svg)](https://pypi.python.org/pypi/sarscov2vec/)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Table of Contents

[Modules](https://github.com/ptynecki/sarscov2vec#modules) | 
[Installation](https://github.com/ptynecki/sarscov2vec#installation-and-usage) |
[Contributions](https://github.com/ptynecki/sarscov2vec#contributions) | 
[Have a question?](https://github.com/ptynecki/sarscov2vec#have-a-question) | 
[Found a bug?](https://github.com/ptynecki/sarscov2vec#found-a-bug) | 
[Team](https://github.com/ptynecki/sarscov2vec#team) | 
[Change log](https://github.com/ptynecki/sarscov2vec#change-log) | 
[License](https://github.com/ptynecki/sarscov2vec#license) | 
[Cite](https://github.com/ptynecki/sarscov2vec#cite)

## Modules

### fastText NLP model

| Filename with SHA256 checksum                                                                                                  | Variants                                  | Description                                                                                          |
|--------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|------------------------------------------------------------------------------------------------------|
| ffasttext_unsupervised_kmer7_25k_samples.28.02.2022.bin<br/>_44f789dcb156201dac9217f8645d86ac585ec24c6eba68901695dc254a14adc3_ | Alpha, Beta, Delta, Gamma, Omicron (BA.1) | fastText unsupervised model trained on 7-mers tokens extracted from 25 000 unique SARS-CoV-2 samples |

### Machine Learning model and label encoder

| Filename with SHA256 checksum                                                                                       | Variants                                        | Description                                                                                                                                         |
|---------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| svm_supervised_36k_samples.28.02.2022.joblib<br/>_70abd23b0181786d4ab8e06ea23bd14641f509c13db58c7f2fa2baea17aa42af_ | Alpha, Beta, Delta, Gamma, Omicron (BA.1, BA.2) | SVM supervised model trained and tested using 36,365 unique SARS-CoV-2 samples. Each genome sample was transformed by fastText model at 28.02.2022. |
| label_encoder_36k_samples.28.02.2022.joblib<br/>_7cb654924f69de6efbf6f409efd91af05874e1392220d22b9883d36c17b366c9_  | Alpha, Beta, Delta, Gamma, Omicron (BA.1, BA.2) | Label extracted from 36,365 unique SARS-CoV-2 samples at 28.02.2022.                                                                                |

## Installation and usage

#### sarscov2vec package

_sarscov2vec_ requires Python 3.8.0+ to run and can be installed by running:

```
pip install sarscov2vec
```

If you can't wait for the latest hotness from the develop branch, then install it directly from the repository:

```
pip install git+git://github.com/ptynecki/sarscov2vec.git@develop
```
Package examples are available in `notebooks` directory.

## Contributions

Development on the latest stable version of Python 3+ is preferred. As of this writing it's 3.8. You can use any operating system.

If you're fixing a bug or adding a new feature, add a test with *[pytest](https://github.com/pytest-dev/pytest)* and check the code with *[Black](https://github.com/psf/black/)* and *[mypy](https://github.com/python/mypy)*. Before adding any large feature, first open an issue for us to discuss the idea with the core devs and community.

## Have a question?

Obviously if you have a private question or want to cooperate with us, you can always reach out to us directly by mail.

## Found a bug?

Feel free to add a new issue with a respective title and description on the [the sarscov2vec repository](https://github.com/ptynecki/sarscov2vec/issues). If you already found a solution to your problem, we would be happy to review your pull request.

## Team

Researchers whose contributing to the sarscov2vec:

* **Piotr Tynecki** (Faculty of Computer Science, Bialystok University of Technology, Bialystok, Poland)
* **Marcin Lubocki** (Laboratory of Virus Molecular Biology, Intercollegiate Faculty of Biotechnology, University of Gdansk, Medical University of Gdańsk, Gdansk, Poland)

## Change log

The log's will become rather long. It moved to its own file.

See [CHANGELOG.md](https://github.com/ptynecki/sarscov2vec/blob/master/CHANGELOG.md).

## License

The sarscov2vec package is released under the under terms of [the MIT License](https://github.com/ptynecki/sarscov2vec/blob/master/LICENSE).

## Cite

> **Application of continuous embedding of viral genome sequences and machine learning in the prediction of SARS-CoV-2 variants**  
>
> Tynecki, P.; Lubocki, M.;
>
> Computer Information Systems and Industrial Management. CISIM 2022. Lecture Notes in Computer Science, Springer
> 