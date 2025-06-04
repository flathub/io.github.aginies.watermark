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
		com.guibo.www.filigraneapp.json

lint:
	flatpak run --command=flatpak-builder-lint \
	       	org.flatpak.Builder manifest com.guibo.www.filigraneapp.json

run:
	flatpak run com.guibo.www.filigraneapp
