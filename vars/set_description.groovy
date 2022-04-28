def call() {
	currentBuild.description = "${NODE}: ${DESCRIPTION}"

	if (env.RUN_DEX2OAT == 'true') {
		currentBuild.description += " + dex2oat"
	}

	if (env.COLLECT_PELT == 'true') {
		currentBuild.description += " + PELT"
	}

	if (env.COLLECT_UCLAMP == 'true') {
		currentBuild.description += " + UCLAMP"
	}
}
