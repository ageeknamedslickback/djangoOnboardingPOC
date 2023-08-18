.PHONY: changelog
changelog:
	git-changelog --style conventional \
		--sections feat,fix,revert,refactor,perf,build,ci,deps,docs,style,test,chore \
		--template path:CHANGELOG.md.jinja \
		--bump-latest \
		-o CHANGELOG.md

.PHONY: build
build:
	unset VERSION
	export VERSION=`python version.py`
	docker build --tag onboarding-${ENVIRONMENT}:${VERSION} .

.PHONY: run
run:
	unset VERSION
	export VERSION=`python version.py`
	docker run -d --name onboarding -p 8000:8000 \
	-e SECRET_KEY=${SECRET_KEY} \
	-e ENVIRONMENT=${ENVIRONMENT} \
	-e SENTRY_DSN=${SENTRY_DSN} \
	-e PORT=${PORT} \
	onboarding-${ENVIRONMENT}:${VERSION}
