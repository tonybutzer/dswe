cat:
	cat Makefile

salloc:
	salloc -N 1 -n 1 -c 4 -A impd -t 1:00:00

sfourhour:
	salloc -N 1 -n 1 -c 4 -A impd -t 4:00:00

shell:
	srun --pty bash -i



run:
	python 0_squirrel.py `head -1 dancecard.txt`



convert:
	jupyter nbconvert --to python --no-prompt 2_numpy_zarr.ipynb
