.PHONY: build

build:
	flatpak run org.flatpak.Builder \
		--force-clean \
		--install \
		--install-deps-from=flathub \
		--ccache \
		--mirror-screenshots-url=https://dl.flathub.org/media/ \
		--user \
		--repo=repo \
		builddir \
		io.github.aginies.watermark.json

lint:
	flatpak run --command=flatpak-builder-lint \
	       	org.flatpak.Builder manifest io.github.aginies.watermark.json

run:
	flatpak run io.github.aginies.watermark
