.PHONY: build

build:
	flatpak install -y flathub org.flatpak.Builder
	flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpak
	flatpak run org.flatpak.Builder \
		--force-clean \
		--install \
		--install-deps-from=flathub \
		--ccache \
		--mirror-screenshots-url=https://dl.flathub.org/media/ \
		--user \
		--repo=repo \
		builddir \
		io.github.aginies.watermark.yml

lint:
	flatpak run --command=flatpak-builder-lint \
	       	org.flatpak.Builder manifest io.github.aginies.watermark.yml

run:
	flatpak run io.github.aginies.watermark

trans:
	rm -vf locale/watermark_app.pot
	xgettext --language=Python --keyword=_ -o locale/watermark_app.pot watermark_app.py
