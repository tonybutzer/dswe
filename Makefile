cat:
	cat Makefile



publish:
	git add .
	git commit -m 'auto commit from tony makefile sept2022'
	git push


git: publish


big:
	du -a . | sort -n -r | head -n 10
	echo HI
	find . -size +10M
	echo HI
	for file in `find . -size +10M`; do ls -lh $$file; done
