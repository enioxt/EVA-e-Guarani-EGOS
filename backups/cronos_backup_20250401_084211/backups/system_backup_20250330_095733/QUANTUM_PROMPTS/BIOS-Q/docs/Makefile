# EVA & GUARANI - Documentation Makefile
# -----------------------------------
# This Makefile provides commands for building the
# EVA & GUARANI BIOS-Q documentation.
#
# Version: 7.5
# Created: 2025-03-26

# You can set these variables from the command line
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help"
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Clean build directory
clean:
	rm -rf $(BUILDDIR)/*

# Build HTML documentation
html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Build PDF documentation
pdf:
	@$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex" $(SPHINXOPTS)
	@echo "Running LaTeX files through pdflatex..."
	@make -C "$(BUILDDIR)/latex" all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

# Build EPUB documentation
epub:
	@$(SPHINXBUILD) -b epub "$(SOURCEDIR)" "$(BUILDDIR)/epub" $(SPHINXOPTS)
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

# Build all documentation formats
all: html pdf epub
	@echo
	@echo "Build finished. The documentation is in $(BUILDDIR)."

# Live reload for development
livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Check for broken links
linkcheck:
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS)
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

# Generate API documentation
apidoc:
	sphinx-apidoc -o "$(SOURCEDIR)/api" ../bios_q
	@echo
	@echo "API documentation generated in $(SOURCEDIR)/api." 