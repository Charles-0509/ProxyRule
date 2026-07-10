.PHONY: sync validate build generate test package

sync:
	python3 scripts/sync_sources.py --update

validate:
	python3 scripts/sync_sources.py --validate-local

build: validate
	python3 scripts/build_mrs.py

generate:
	python3 scripts/generate_configs.py

test: build generate
	python3 -m unittest discover -s tests -v
	python3 scripts/generate_configs.py --test-mode --output-dir .cache
	mkdir -p .cache/mihomo-home
	SAFE_PATHS="$$(pwd)" $$(python3 scripts/ensure_mihomo.py) -t -d .cache/mihomo-home -f .cache/openclash-test.yaml

package: test
	@test -n "$(TAG)" || (echo 'use make package TAG=vYYYY.MM.DD' && exit 2)
	python3 scripts/package_release.py "$(TAG)"
