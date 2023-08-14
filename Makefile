.PHONY: changelog
changelog:
	git-changelog --style conventional \
		--sections feat,fix,revert,refactor,perf,build,ci,deps,docs,style,test,chore \
		--template path:CHANGELOG.md.jinja \
		--bump-latest \
		-o CHANGELOG.md