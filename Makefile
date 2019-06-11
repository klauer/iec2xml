all: index.html iec_grammar.py sample.xml types.xml

iec_grammar.py: iec.grammar
	python iec2peg.py > iec_grammar.py

sample.xml: iec_grammar.py sample.EXP
	./iec2xml -o $@ sample.EXP

types.xml: iec_grammar.py types.EXP
	./iec2xml -o $@ types.EXP

%.html: %.en.yhtml2 nav.en.yhtml2 iec2xml_homepage.en.yhtml2 iec2xml_homepage.yhtml2
	yml2c $< -o $@

update: all
	if test -z $(VERSION) ; then echo VERSION not set ; exit 1 ; fi
	ssh www bash -c "cd ; cd x-pie.de/; tar cvjf iec2xml-$(VERSION).tar.bz2 iec2xml/{Makefile,*.png,*.jpg,*.css,*.txt,*.grammar,*.py,iec2xml,*.yhtml2,*.EXP} ; rm iec2xml.tar.bz2 ; ln -s iec2xml-$(VERSION).tar.bz2 iec2xml.tar.bz2"

clean:
	rm -f *.html iec_grammar.py *.pyc *.xml
