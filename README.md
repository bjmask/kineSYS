# kineSYS
Implementing support vector machines to classify SSVEP signals from the Emotiv Epoc headset

Steady-state visually evoked potentials (SSVEP's) are phenomena observed in the brain when the subject observes specific frequencies, e.g a  constant rate strobe.

The stimulus is implemented in ssvep_trainer.py which spawns a subprocess, anyone with access to the emotiv headset and the sdk can launch the trainer, follow the prompts on the screen and complete a training cycle.

The time-series data is read from raw csv, applied a notch filter (50-60 Hz) and a bandpass (5-30 Hz), the signal the undergoes dimensionality reduction with PCA (ICA and RandomizedPCA do not work as well) and finally a fast-fourier transform.

Follow our implementation in SSVEP Workshop.ipynb !
