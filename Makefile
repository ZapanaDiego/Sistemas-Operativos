.PHONY: all pdf count clean help

all: pdf

pdf:
	@./build.sh

count:
	@echo "--- Conteo detallado de palabras ---"
	@texcount -inc -sub=none main.tex 2>/dev/null
	@echo ""
	@echo "Regla de extensión: 5 a 10 páginas de SOLO TEXTO."
	@echo "Equivalencia IEEEtran dos columnas: ~850 palabras/página."
	@echo "Rango objetivo: ~4,250 a 8,500 palabras."

clean:
	@echo "Limpiando archivos auxiliares..."
	@rm -f main.aux main.log main.out main.bbl main.blg main.toc
	@echo "Listo."

help:
	@echo "Comandos disponibles:"
	@echo "  make pdf    - Compila el artículo a PDF en main.pdf"
	@echo "  make count  - Cuenta palabras y estima páginas de solo texto"
	@echo "  make clean  - Elimina archivos temporales de compilación"
